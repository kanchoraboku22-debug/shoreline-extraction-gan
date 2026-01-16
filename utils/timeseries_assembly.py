"""
Time-Series Assembly for LSTM Temporal Forecasting - Phase 3B

Converts transect-based shoreline measurements into ordered temporal sequences
ready for LSTM training. Each transect becomes a time-series input for
predictive modeling.

Outputs:
  - shoreline_timeseries.csv: Long-form temporal data
  - lstm_sequences.npy: Stacked tensor format for direct LSTM ingestion
  - temporal_metadata.json: Sequence mapping and metadata
"""

import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transect_analysis(analysis_dir: str) -> Optional[pd.DataFrame]:
    """
    Load transect analysis results from Phase 3A.
    
    Args:
        analysis_dir: Path to model_outputs/analysis/transects
    
    Returns:
        DataFrame with transect change metrics
    """
    csv_path = os.path.join(analysis_dir, 'shoreline_change_stats.csv')
    
    if not os.path.exists(csv_path):
        logger.error(f"Analysis file not found: {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded {len(df)} transects with change data")
    
    return df


def extract_temporal_sequence(
    row: pd.Series,
    years: List[int] = [1994, 2004, 2014, 2024]
) -> Tuple[List[float], List[int]]:
    """
    Extract temporal sequence from transect row.
    
    Args:
        row: Transect data row
        years: Years in chronological order
    
    Returns:
        Tuple of (positions, years) where positions are shoreline distances
    """
    
    positions = []
    valid_years = []
    
    for year in years:
        col_name = f'position_{year}'
        if col_name in row and pd.notna(row[col_name]):
            positions.append(float(row[col_name]))
            valid_years.append(year)
    
    return positions, valid_years


def create_timeseries_dataframe(
    df_transects: pd.DataFrame,
    years: List[int] = [1994, 2004, 2014, 2024]
) -> Optional[pd.DataFrame]:
    """
    Create long-form time-series dataframe from transect data.
    
    Args:
        df_transects: Transect analysis results
        years: Years in chronological order
    
    Returns:
        Long-form dataframe with columns: transect_id, year, position, ...
    """
    
    timeseries_rows = []
    
    for idx, row in df_transects.iterrows():
        transect_id = row['transect_id']
        
        positions, valid_years = extract_temporal_sequence(row, years)
        
        if len(positions) < 2:
            continue
        
        for year, position in zip(valid_years, positions):
            # Calculate annual change from previous year
            year_idx = valid_years.index(year)
            
            if year_idx == 0:
                annual_change = 0
                time_since_first = 0
            else:
                prev_position = positions[year_idx - 1]
                prev_year = valid_years[year_idx - 1]
                annual_change = (position - prev_position) / (year - prev_year)
                time_since_first = year - valid_years[0]
            
            timeseries_rows.append({
                'transect_id': transect_id,
                'year': year,
                'position': position,
                'annual_change': annual_change,
                'time_since_first': time_since_first,
                'epr': row['epr_pixels_per_year'],
                'change_type': row['change_type']
            })
    
    df_ts = pd.DataFrame(timeseries_rows)
    logger.info(f"Created time-series with {len(df_ts)} observations")
    
    return df_ts


def create_lstm_sequences(
    df_ts: pd.DataFrame,
    years: List[int] = [1994, 2004, 2014, 2024],
    forecast_year: int = 2034
) -> Tuple[np.ndarray, List[Dict], List[int]]:
    """
    Create LSTM-ready sequence tensor.
    
    Each sequence is [position_1994, position_2004, position_2014, position_2024]
    Padded with NaN for missing values.
    
    Args:
        df_ts: Time-series dataframe
        years: Historical years
        forecast_year: Year to forecast
    
    Returns:
        Tuple of (sequences array, metadata list, transect IDs)
    """
    
    transect_ids = df_ts['transect_id'].unique()
    sequences = []
    metadata = []
    valid_transects = []
    
    for tid in sorted(transect_ids):
        subset = df_ts[df_ts['transect_id'] == tid].sort_values('year')
        
        # Create sequence vector
        sequence = []
        has_data = False
        
        for year in years:
            year_data = subset[subset['year'] == year]
            
            if len(year_data) > 0:
                sequence.append(year_data['position'].values[0])
                has_data = True
            else:
                sequence.append(np.nan)
        
        if not has_data:
            continue
        
        sequences.append(sequence)
        
        # Store metadata
        meta = {
            'transect_id': tid,
            'num_observations': len(subset),
            'years_present': subset['year'].tolist(),
            'change_type': subset['change_type'].iloc[0],
            'mean_annual_change': subset[subset['year'] > subset['year'].min()]['annual_change'].mean()
        }
        metadata.append(meta)
        valid_transects.append(tid)
    
    # Convert to numpy array
    sequences_array = np.array(sequences, dtype=np.float32)
    
    logger.info(f"Created {len(sequences_array)} LSTM-ready sequences")
    logger.info(f"Sequence shape: {sequences_array.shape}")
    
    return sequences_array, metadata, valid_transects


def export_timeseries(
    df_ts: pd.DataFrame,
    sequences: np.ndarray,
    metadata: List[Dict],
    transect_ids: List[int],
    output_dir: str
) -> Dict[str, str]:
    """
    Export time-series data in multiple formats.
    
    Args:
        df_ts: Long-form time-series dataframe
        sequences: LSTM-ready sequence tensor
        metadata: Sequence metadata
        transect_ids: Transect IDs corresponding to sequences
        output_dir: Output directory
    
    Returns:
        Dictionary of created files
    """
    
    os.makedirs(output_dir, exist_ok=True)
    outputs = {}
    
    # Export long-form CSV
    csv_path = os.path.join(output_dir, 'shoreline_timeseries.csv')
    df_ts.to_csv(csv_path, index=False)
    logger.info(f"✓ Time-series CSV: {csv_path}")
    outputs['timeseries_csv'] = csv_path
    
    # Export LSTM sequences
    npy_path = os.path.join(output_dir, 'lstm_sequences.npy')
    np.save(npy_path, sequences)
    logger.info(f"✓ LSTM sequences: {npy_path}")
    outputs['lstm_sequences'] = npy_path
    
    # Export metadata
    meta_path = os.path.join(output_dir, 'sequence_metadata.json')
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_metadata(obj):
        if isinstance(obj, dict):
            return {k: convert_metadata(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_metadata(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    meta_dict = {
        'sequences': convert_metadata(metadata),
        'transect_ids': [int(tid) for tid in transect_ids],
        'years': [1994, 2004, 2014, 2024],
        'shape': list(sequences.shape),
        'dtype': str(sequences.dtype)
    }
    
    with open(meta_path, 'w') as f:
        json.dump(meta_dict, f, indent=2)
    
    logger.info(f"✓ Metadata: {meta_path}")
    outputs['metadata'] = meta_path
    
    return outputs


def assemble_timeseries(
    analysis_dir: str = 'model_outputs/analysis/transects',
    output_dir: str = 'model_outputs/analysis/timeseries'
) -> bool:
    """
    Run complete time-series assembly pipeline.
    
    Args:
        analysis_dir: Path to Phase 3A results
        output_dir: Output directory for Phase 3B results
    
    Returns:
        True if successful
    """
    
    logger.info("=" * 75)
    logger.info("PHASE 3B: TIME-SERIES ASSEMBLY FOR LSTM")
    logger.info("=" * 75)
    
    # Load transect analysis
    df_transects = load_transect_analysis(analysis_dir)
    if df_transects is None:
        return False
    
    # Create long-form time-series
    df_ts = create_timeseries_dataframe(df_transects)
    if df_ts is None or len(df_ts) == 0:
        logger.error("Failed to create time-series")
        return False
    
    # Create LSTM-ready sequences
    sequences, metadata, transect_ids = create_lstm_sequences(df_ts)
    
    # Export results
    outputs = export_timeseries(df_ts, sequences, metadata, transect_ids, output_dir)
    
    logger.info("\n" + "=" * 75)
    logger.info("PHASE 3B COMPLETE")
    logger.info("=" * 75)
    
    return True


if __name__ == '__main__':
    success = assemble_timeseries(
        analysis_dir='model_outputs/analysis/transects',
        output_dir='model_outputs/analysis/timeseries'
    )
