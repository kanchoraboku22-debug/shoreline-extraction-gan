#!/usr/bin/env python3
"""
PHASE 3 QUICK START GUIDE - Temporal Change & Forecasting Pipeline

This script documents the quick start for Phase 3 analysis and forecasting.

Three ways to use Phase 3:

1. EXECUTE COMPLETE PIPELINE
   python scripts/run_phase3_full.py
   
2. GENERATE VISUALIZATIONS ONLY
   python scripts/visualize_phase3_results.py
   
3. USE INDIVIDUAL MODULES IN CUSTOM SCRIPTS
   from utils.transect_analysis import run_transect_analysis
   from utils.timeseries_assembly import assemble_timeseries
   from utils.lstm_forecasting import run_lstm_forecasting

================================================================================
COMPLETE PIPELINE EXECUTION
================================================================================
"""

import subprocess
import sys
from pathlib import Path

def run_phase3_pipeline():
    """Execute complete Phase 3 pipeline."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║        PHASE 3: TEMPORAL CHANGE & FORECASTING - QUICK START              ║
    ║                                                                            ║
    ║  This pipeline will execute all three Phase 3 components:                 ║
    ║                                                                            ║
    ║  1. Phase 3A: Transect-based coastal change analysis                      ║
    ║     - Input: Phase 2 vector shorelines (shoreline_1994-2024.shp)          ║
    ║     - Output: transects.shp, shoreline_change_stats.csv                   ║
    ║     - Time: ~2-5 seconds                                                  ║
    ║                                                                            ║
    ║  2. Phase 3B: Time-series assembly for LSTM                               ║
    ║     - Input: Phase 3A transect analysis                                   ║
    ║     - Output: shoreline_timeseries.csv, lstm_sequences.npy                ║
    ║     - Time: ~1 second                                                     ║
    ║                                                                            ║
    ║  3. Phase 3C: LSTM forecasting (2034, 2044)                               ║
    ║     - Input: Phase 3B time-series data                                    ║
    ║     - Output: shoreline_forecast.csv, forecast_summary.txt                ║
    ║     - Time: ~1-2 seconds                                                  ║
    ║                                                                            ║
    ║  Total Pipeline Time: ~5-10 seconds                                       ║
    ║                                                                            ║
    ║  Output Location: model_outputs/analysis/                                 ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run pipeline
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/run_phase3_full.py'],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pipeline: {e}")
        return False


def generate_visualizations():
    """Generate publication-ready visualizations."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    GENERATING PHASE 3 VISUALIZATIONS                       ║
    ║                                                                            ║
    ║  This will create 4 publication-ready plots:                              ║
    ║                                                                            ║
    ║  1. erosion_accretion_map.png                                              ║
    ║     - Scatter plot of transect NSM values                                  ║
    ║     - Color-coded by erosion/accretion classification                      ║
    ║                                                                            ║
    ║  2. change_metrics_distribution.png                                        ║
    ║     - Histograms of NSM, EPR, MAC metrics                                  ║
    ║     - Statistical distributions with mean markers                          ║
    ║                                                                            ║
    ║  3. lstm_forecast_samples.png                                              ║
    ║     - 10 sample transects with historical + forecast data                  ║
    ║     - Blue lines: 1994-2024 historical                                     ║
    ║     - Red dashed: 2034, 2044 forecast                                      ║
    ║                                                                            ║
    ║  4. summary_statistics.png                                                 ║
    ║     - Text-based summary of all metrics                                    ║
    ║     - Classification percentages and statistics                            ║
    ║                                                                            ║
    ║  Output Location: model_outputs/validation_plots/                          ║
    ║  Resolution: 300 DPI (publication-ready)                                   ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/visualize_phase3_results.py'],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        return False


def show_file_structure():
    """Display Phase 3 output file structure."""
    
    print("""
    ═══════════════════════════════════════════════════════════════════════════════
    
    PHASE 3 OUTPUT FILE STRUCTURE
    
    model_outputs/
    ├── analysis/
    │   ├── transects/                     [Phase 3A: Transect Analysis]
    │   │   ├── transects.shp              → GIS shapefile (QGIS/ArcGIS)
    │   │   ├── transects.shx              → Shapefile index
    │   │   ├── transects.dbf              → Attribute data
    │   │   ├── transects.prj              → Projection info
    │   │   ├── shoreline_change_stats.csv → Statistical metrics
    │   │   └── change_summary.txt         → Text summary
    │   │
    │   ├── timeseries/                    [Phase 3B: Time-Series Assembly]
    │   │   ├── shoreline_timeseries.csv   → Long-form time-series
    │   │   ├── lstm_sequences.npy         → LSTM tensor array
    │   │   └── sequence_metadata.json     → Metadata (years, shape, etc)
    │   │
    │   └── forecast/                      [Phase 3C: LSTM Forecasting]
    │       ├── shoreline_forecast.csv     → Historical + forecast data
    │       ├── scaler.pkl                 → Data normalization scaler
    │       └── forecast_summary.txt       → Forecast results summary
    │
    └── validation_plots/                  [Visualizations]
        ├── erosion_accretion_map.png      → Change classification plot
        ├── change_metrics_distribution.png → NSM/EPR/MAC histograms
        ├── lstm_forecast_samples.png      → Forecast visualization
        └── summary_statistics.png         → Summary statistics plot
    
    ═══════════════════════════════════════════════════════════════════════════════
    """)


def show_usage_examples():
    """Show code examples for using Phase 3 modules."""
    
    print("""
    ═══════════════════════════════════════════════════════════════════════════════
    
    USAGE EXAMPLES - IMPORTING PHASE 3 MODULES
    
    ═══════════════════════════════════════════════════════════════════════════════
    
    EXAMPLE 1: Run Phase 3A (Transect Analysis) Only
    ────────────────────────────────────────────────
    
    from utils.transect_analysis import run_transect_analysis
    
    success = run_transect_analysis(
        processed_dir='model_outputs/processed',
        output_dir='model_outputs/analysis',
        transect_spacing=50,      # 50 pixels
        transect_length=300       # 300 pixels
    )
    
    if success:
        print("Transect analysis complete!")
        print("Outputs in: model_outputs/analysis/transects/")
    
    ═══════════════════════════════════════════════════════════════════════════════
    
    EXAMPLE 2: Run Phase 3B (Time-Series Assembly) Only
    ────────────────────────────────────────────────────
    
    from utils.timeseries_assembly import assemble_timeseries
    
    success = assemble_timeseries(
        analysis_dir='model_outputs/analysis/transects',
        output_dir='model_outputs/analysis/timeseries'
    )
    
    if success:
        print("Time-series assembly complete!")
        # Load and inspect sequences
        import numpy as np
        sequences = np.load('model_outputs/analysis/timeseries/lstm_sequences.npy')
        print(f"Sequences shape: {sequences.shape}")  # (62, 4)
    
    ═══════════════════════════════════════════════════════════════════════════════
    
    EXAMPLE 3: Run Phase 3C (LSTM Forecasting) Only
    ────────────────────────────────────────────────
    
    from utils.lstm_forecasting import run_lstm_forecasting
    
    success = run_lstm_forecasting(
        timeseries_dir='model_outputs/analysis/timeseries',
        output_dir='model_outputs/analysis/forecast',
        epochs=50
    )
    
    if success:
        print("LSTM forecasting complete!")
        # Load forecasts
        import pandas as pd
        df = pd.read_csv('model_outputs/analysis/forecast/shoreline_forecast.csv')
        print(f"Total rows: {len(df)}")
        print(df[df['type'] == 'forecast'].head())
    
    ═══════════════════════════════════════════════════════════════════════════════
    
    EXAMPLE 4: Custom Analysis with Phase 3 Modules
    ────────────────────────────────────────────────
    
    import pandas as pd
    import numpy as np
    from utils.transect_analysis import run_transect_analysis
    
    # Run Phase 3A
    run_transect_analysis(
        processed_dir='model_outputs/processed',
        output_dir='model_outputs/analysis'
    )
    
    # Load and analyze results
    stats_df = pd.read_csv('model_outputs/analysis/transects/shoreline_change_stats.csv')
    
    # Get erosion statistics
    erosion = stats_df[stats_df['change_type'] == 'Erosion']
    print(f"Erosion zones: {len(erosion)}")
    print(f"Mean erosion rate: {erosion['epr_pixels_per_year'].mean():.3f} px/yr")
    
    # Get accretion statistics
    accretion = stats_df[stats_df['change_type'] == 'Accretion']
    print(f"Accretion zones: {len(accretion)}")
    print(f"Mean accretion rate: {accretion['epr_pixels_per_year'].mean():.3f} px/yr")
    
    # Custom plotting
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 6))
    plt.bar(['Erosion', 'Stable', 'Accretion'],
            [len(erosion), len(stats_df[stats_df['change_type'] == 'Stable']), len(accretion)])
    plt.ylabel('Number of Transects')
    plt.title('Coastal Change Classification')
    plt.savefig('coastal_change_summary.png', dpi=300)
    
    ═══════════════════════════════════════════════════════════════════════════════
    
    EXAMPLE 5: Load and Analyze Forecast Results
    ────────────────────────────────────────────
    
    import pandas as pd
    
    # Load forecast data
    df = pd.read_csv('model_outputs/analysis/forecast/shoreline_forecast.csv')
    
    # Historical data
    historical = df[df['type'] == 'historical']
    print(f"Historical observations: {len(historical)}")
    print(historical.groupby('year').size())
    
    # Forecast data
    forecast = df[df['type'] == 'forecast']
    print(f"Forecast predictions: {len(forecast)}")
    print(forecast.groupby('year').size())
    
    # Analyze 2044 forecast
    forecast_2044 = forecast[forecast['year'] == 2044]
    print(f"\\n2044 Forecast Statistics:")
    print(f"  Mean position: {forecast_2044['position'].mean():.2f} pixels")
    print(f"  Std deviation: {forecast_2044['position'].std():.2f} pixels")
    print(f"  Range: [{forecast_2044['position'].min():.2f}, {forecast_2044['position'].max():.2f}]")
    
    ═══════════════════════════════════════════════════════════════════════════════
    """)


def main():
    """Main menu for Phase 3 quick start."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║          PHASE 3 QUICK START - Shoreline Extraction GAN Project           ║
    ║                                                                            ║
    ║               Temporal Change Analysis & Forecasting System               ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    
    QUICK START OPTIONS:
    
    1. Run Complete Phase 3 Pipeline
       (Transect Analysis → Time-Series Assembly → LSTM Forecasting)
       
    2. Generate Visualizations Only
       (Assumes Phase 3 already executed)
       
    3. View Output File Structure
       
    4. Show Usage Examples
       
    5. Exit
    
    ════════════════════════════════════════════════════════════════════════════════
    """)
    
    while True:
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            print()
            if run_phase3_pipeline():
                print("\n✅ Phase 3 pipeline completed successfully!")
                print("   Check model_outputs/analysis/ for outputs")
            else:
                print("\n❌ Phase 3 pipeline failed. Check logs above.")
            break
            
        elif choice == '2':
            print()
            if generate_visualizations():
                print("\n✅ Visualizations generated successfully!")
                print("   Check model_outputs/validation_plots/ for plots")
            else:
                print("\n❌ Visualization generation failed. Check logs above.")
            break
            
        elif choice == '3':
            show_file_structure()
            
        elif choice == '4':
            show_usage_examples()
            
        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
            
        else:
            print("Invalid choice. Try again.")
    
    print("""
    
    ════════════════════════════════════════════════════════════════════════════════
    For more information, see:
    - PHASE_3_COMPLETION_REPORT.txt  (Detailed technical documentation)
    - scripts/run_phase3_full.py     (Pipeline orchestration)
    - utils/transect_analysis.py     (Phase 3A module)
    - utils/timeseries_assembly.py   (Phase 3B module)
    - utils/lstm_forecasting.py      (Phase 3C module)
    ════════════════════════════════════════════════════════════════════════════════
    """)


if __name__ == '__main__':
    main()
