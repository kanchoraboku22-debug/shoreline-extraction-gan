"""
LSTM Forecasting Module - Phase 3C

Trains LSTM model on historical shoreline time-series data and forecasts
future shoreline positions. Uses TensorFlow if available, falls back to linear regression.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Optional, Dict
import logging
import pickle
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from tensorflow import keras
    from tensorflow.keras import layers, Sequential
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    keras = None
    Sequential = None
    layers = None
    logger.warning("TensorFlow not installed. Will use linear regression fallback.")

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression


def load_lstm_data(timeseries_dir):
    """Load prepared LSTM sequences and metadata."""
    
    timeseries_dir = Path(timeseries_dir)
    
    logger.info(f"Loading LSTM data from {timeseries_dir}")
    
    csv_path = timeseries_dir / 'shoreline_timeseries.csv'
    if csv_path.exists():
        df_ts = pd.read_csv(csv_path)
        logger.info(f"Loaded CSV: {len(df_ts)} rows")
    else:
        logger.error(f"CSV not found: {csv_path}")
        return None
    
    npy_path = timeseries_dir / 'lstm_sequences.npy'
    if npy_path.exists():
        sequences = np.load(npy_path)
        logger.info(f"Loaded sequences: {sequences.shape}")
    else:
        sequences = None
    
    meta_path = timeseries_dir / 'sequence_metadata.json'
    if meta_path.exists():
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}
    
    return df_ts, sequences, metadata


def prepare_lstm_training_data(sequences, lookback=3):
    """Prepare training data for LSTM."""
    
    if sequences is None:
        logger.error("No sequences provided")
        return None, None
    
    X, y = [], []
    
    for seq in sequences:
        # Fill NaN
        mask = np.isnan(seq)
        idx = np.where(~mask, np.arange(mask.size), 0)
        idx = np.maximum.accumulate(idx)
        seq_filled = seq[idx]
        
        if len(seq_filled) >= lookback + 1:
            X.append(seq_filled[:lookback])
            y.append(seq_filled[lookback])
    
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    
    logger.info(f"Training data: X {X.shape}, y {y.shape}")
    
    return X, y


def build_lstm_model(input_shape, lstm_units=32, dropout_rate=0.2):
    """Build LSTM model for shoreline forecasting."""
    
    if not HAS_TENSORFLOW:
        logger.warning("TensorFlow not available")
        return None
    
    model = Sequential([
        layers.Input(shape=input_shape),
        layers.LSTM(lstm_units, activation='relu', return_sequences=True),
        layers.Dropout(dropout_rate),
        layers.LSTM(lstm_units // 2, activation='relu'),
        layers.Dropout(dropout_rate),
        layers.Dense(16, activation='relu'),
        layers.Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    logger.info(f"Built LSTM with {lstm_units} units")
    
    return model


def train_lstm_model(X, y, epochs=50, batch_size=16, validation_split=0.2):
    """Train LSTM model on shoreline data."""
    
    logger.info("Training model...")
    
    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()
    
    if HAS_TENSORFLOW:
        model = build_lstm_model(input_shape=(X_scaled.shape[1],))
        if model is not None:
            X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))
            model.fit(
                X_reshaped, y_scaled,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=validation_split,
                verbose=1
            )
            logger.info("✅ LSTM training complete")
            return model, scaler
    
    logger.warning("Using linear regression fallback")
    model = LinearRegression()
    model.fit(X_scaled, y_scaled)
    logger.info("✅ Linear model trained")
    return model, scaler


def forecast_shoreline(model, scaler, X_test, years=[2034, 2044]):
    """Generate shoreline forecasts for future years."""
    
    logger.info(f"Generating forecasts for {years}")
    
    forecasts = {}
    
    for year in years:
        if HAS_TENSORFLOW and hasattr(model, 'predict'):
            X_reshaped = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
            y_pred = model.predict(X_reshaped, verbose=0)
            y_pred_orig = y_pred.ravel() * scaler.scale_[0] + scaler.mean_[0]
        else:
            # Linear regression on scaled data
            y_pred = model.predict(X_test).reshape(-1, 1)
            # Inverse transform: y_orig = (y_scaled * scale) + mean
            y_pred_orig = (y_pred * scaler.scale_[0]).ravel() + scaler.mean_[0]
        
        forecasts[year] = y_pred_orig
    
    logger.info(f"✅ Forecasts generated")
    
    return forecasts


def export_forecast_results(model, scaler, forecasts, dataframe, output_dir):
    """Export forecast results to files."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Exporting to {output_dir}")
    
    # Save model
    if HAS_TENSORFLOW and hasattr(model, 'save'):
        model.save(str(output_dir / 'lstm_model.h5'))
        logger.info("✓ Model saved")
    
    # Save scaler
    with open(output_dir / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    logger.info("✓ Scaler saved")
    
    # Create forecast dataframe
    records = []
    for _, row in dataframe.iterrows():
        records.append({
            'transect_id': row['transect_id'],
            'year': row['year'],
            'position': row['position'],
            'type': 'historical'
        })
    
    for year, values in forecasts.items():
        for tid in range(len(values)):
            records.append({
                'transect_id': tid,
                'year': year,
                'position': values[tid],
                'type': 'forecast'
            })
    
    df_forecast = pd.DataFrame(records)
    df_forecast.to_csv(output_dir / 'shoreline_forecast.csv', index=False)
    logger.info("✓ Forecast CSV saved")
    
    # Summary
    summary_path = output_dir / 'forecast_summary.txt'
    with open(summary_path, 'w') as f:
        f.write("LSTM SHORELINE FORECAST SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Model: {'TensorFlow LSTM' if HAS_TENSORFLOW else 'Linear Regression'}\n")
        f.write(f"Transects: {dataframe['transect_id'].nunique()}\n")
        f.write(f"Historical: {sorted(dataframe['year'].unique())}\n")
        f.write(f"Forecast: {list(forecasts.keys())}\n\n")
        f.write(df_forecast.to_string())
    
    logger.info("✓ Summary saved")
    
    return True


def run_lstm_forecasting(timeseries_dir, output_dir, epochs=50):
    """Execute complete LSTM forecasting workflow."""
    
    logger.info("=" * 80)
    logger.info("PHASE 3C: LSTM FORECASTING")
    logger.info("=" * 80)
    
    # Load data
    df, sequences, metadata = load_lstm_data(timeseries_dir)
    if df is None:
        logger.error("Failed to load data")
        return False
    
    # Fallback: create sequences from dataframe if needed
    if sequences is None:
        logger.warning("Creating sequences from dataframe...")
        transect_ids = sorted(df['transect_id'].unique())
        sequences = []
        
        for tid in transect_ids:
            transect_data = df[df['transect_id'] == tid].sort_values('year')
            positions = transect_data['position'].values
            sequences.append(positions)
        
        sequences = np.array(sequences, dtype=np.float32)
    
    # Prepare training data
    X, y = prepare_lstm_training_data(sequences)
    if X is None:
        logger.error("Failed to prepare data")
        return False
    
    # Train model
    model, scaler = train_lstm_model(X, y, epochs=epochs)
    if model is None:
        logger.error("Failed to train model")
        return False
    
    # Generate forecasts
    forecasts = forecast_shoreline(model, scaler, X, years=[2034, 2044])
    
    # Export results
    export_forecast_results(model, scaler, forecasts, df, output_dir)
    
    logger.info("✅ Phase 3C complete\n")
    
    return True


if __name__ == '__main__':
    success = run_lstm_forecasting(
        'model_outputs/analysis/timeseries',
        'model_outputs/analysis/forecast',
        epochs=50
    )
