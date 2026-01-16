#!/usr/bin/env python3
"""
PHASE 3 VISUALIZATION & VALIDATION

Generates publication-quality visualizations from Phase 3 analysis:
  - Shoreline change maps (erosion/accretion spatial distribution)
  - Temporal change plots (NSM, EPR trends over time)
  - LSTM forecast visualization (historical + predicted shorelines)
  - Change statistics summary plots
"""

import sys
import os
from pathlib import Path
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import warnings

warnings.filterwarnings('ignore')

# Add utils to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from utils.vector_export_utils import load_geojson_simple
except ImportError:
    load_geojson_simple = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def plot_erosion_accretion_map(analysis_dir, output_dir):
    """
    Create map visualization of erosion/accretion zones.
    """
    try:
        logger.info("Generating erosion/accretion map...")
        
        stats_file = Path(analysis_dir) / 'shoreline_change_stats.csv'
        if not stats_file.exists():
            logger.warning(f"Stats file not found: {stats_file}")
            return False
        
        # Load data
        df = pd.read_csv(stats_file)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Classify zones
        erosion = df[df['change_type'] == 'Erosion']
        accretion = df[df['change_type'] == 'Accretion']
        stable = df[df['change_type'] == 'Stable']
        
        # Plot by type
        if len(erosion) > 0:
            ax.scatter(erosion['transect_id'], erosion['nsm_pixels'], 
                      c='red', s=100, alpha=0.6, label='Erosion')
        if len(accretion) > 0:
            ax.scatter(accretion['transect_id'], accretion['nsm_pixels'], 
                      c='green', s=100, alpha=0.6, label='Accretion')
        if len(stable) > 0:
            ax.scatter(stable['transect_id'], stable['nsm_pixels'], 
                      c='gray', s=100, alpha=0.6, label='Stable')
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Labels and formatting
        ax.set_xlabel('Transect ID', fontsize=12, fontweight='bold')
        ax.set_ylabel('Net Shoreline Movement (NSM) [pixels]', fontsize=12, fontweight='bold')
        ax.set_title('Shoreline Change Classification: Erosion/Accretion', 
                     fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Save
        output_file = Path(output_dir) / 'erosion_accretion_map.png'
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"✅ Saved: {output_file}")
        plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating erosion/accretion map: {e}")
        return False


def plot_change_metrics(analysis_dir, output_dir):
    """
    Visualize NSM, EPR, and MAC metrics.
    """
    try:
        logger.info("Generating change metrics plot...")
        
        stats_file = Path(analysis_dir) / 'shoreline_change_stats.csv'
        if not stats_file.exists():
            logger.warning(f"Stats file not found: {stats_file}")
            return False
        
        df = pd.read_csv(stats_file)
        
        # Create subplots
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # NSM
        axes[0].hist(df['nsm_pixels'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Net Shoreline Movement (pixels)', fontsize=11)
        axes[0].set_ylabel('Frequency', fontsize=11)
        axes[0].set_title('NSM Distribution', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].axvline(df['nsm_pixels'].mean(), color='red', linestyle='--', linewidth=2, 
                       label=f'Mean: {df["nsm_pixels"].mean():.2f}')
        axes[0].legend()
        
        # EPR
        axes[1].hist(df['epr_pixels_per_year'], bins=30, color='coral', edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('End Point Rate (pixels/year)', fontsize=11)
        axes[1].set_ylabel('Frequency', fontsize=11)
        axes[1].set_title('EPR Distribution', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].axvline(df['epr_pixels_per_year'].mean(), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {df["epr_pixels_per_year"].mean():.2f}')
        axes[1].legend()
        
        # MAC
        axes[2].hist(df['mac_pixels_per_year'], bins=30, color='seagreen', edgecolor='black', alpha=0.7)
        axes[2].set_xlabel('Mean Annual Change (pixels/year)', fontsize=11)
        axes[2].set_ylabel('Frequency', fontsize=11)
        axes[2].set_title('MAC Distribution', fontsize=12, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        axes[2].axvline(df['mac_pixels_per_year'].mean(), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {df["mac_pixels_per_year"].mean():.2f}')
        axes[2].legend()
        
        plt.tight_layout()
        output_file = Path(output_dir) / 'change_metrics_distribution.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"✅ Saved: {output_file}")
        plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating change metrics plot: {e}")
        return False


def plot_lstm_forecast(forecast_dir, output_dir):
    """
    Visualize LSTM forecasts with historical data.
    """
    try:
        logger.info("Generating LSTM forecast plot...")
        
        forecast_file = Path(forecast_dir) / 'shoreline_forecast.csv'
        if not forecast_file.exists():
            logger.warning(f"Forecast file not found: {forecast_file}")
            return False
        
        df = pd.read_csv(forecast_file)
        
        # Sample transects for visualization (max 10)
        n_transects = min(10, df['transect_id'].nunique())
        transect_ids = df['transect_id'].unique()[:n_transects]
        
        fig, axes = plt.subplots(2, 5 if n_transects == 10 else (n_transects + 1) // 2, 
                                 figsize=(16, 8))
        axes = axes.flatten()
        
        for idx, transect_id in enumerate(transect_ids):
            transect_data = df[df['transect_id'] == transect_id]
            
            ax = axes[idx]
            
            # Historical data
            historical = transect_data[transect_data['year'] <= 2024]
            if len(historical) > 0:
                ax.plot(historical['year'], historical['position'], 
                       'o-', color='steelblue', linewidth=2, markersize=8, 
                       label='Historical')
            
            # Forecast
            forecast = transect_data[transect_data['year'] > 2024]
            if len(forecast) > 0:
                # Connect last historical to first forecast
                last_hist = historical.iloc[-1] if len(historical) > 0 else None
                if last_hist is not None:
                    forecast_with_conn = pd.concat([
                        pd.DataFrame([{'year': last_hist['year'], 
                                      'position': last_hist['position']}]),
                        forecast
                    ])
                    ax.plot(forecast_with_conn['year'], forecast_with_conn['position'], 
                           's--', color='coral', linewidth=2, markersize=8, 
                           label='Forecast')
            
            ax.set_xlabel('Year', fontsize=10)
            ax.set_ylabel('Shoreline Position (pixels)', fontsize=10)
            ax.set_title(f'Transect {transect_id}', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=9)
            
            # Add vertical line at 2024
            ax.axvline(x=2024, color='black', linestyle=':', alpha=0.5)
        
        # Hide unused subplots
        for idx in range(len(transect_ids), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('LSTM Shoreline Forecasts (Sample Transects)', 
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        output_file = Path(output_dir) / 'lstm_forecast_samples.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"✅ Saved: {output_file}")
        plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating LSTM forecast plot: {e}")
        return False


def plot_summary_statistics(analysis_dir, output_dir):
    """
    Create summary statistics visualization.
    """
    try:
        logger.info("Generating summary statistics...")
        
        stats_file = Path(analysis_dir) / 'shoreline_change_stats.csv'
        if not stats_file.exists():
            logger.warning(f"Stats file not found: {stats_file}")
            return False
        
        df = pd.read_csv(stats_file)
        
        # Calculate statistics
        total_transects = len(df)
        erosion_count = len(df[df['change_type'] == 'Erosion'])
        accretion_count = len(df[df['change_type'] == 'Accretion'])
        stable_count = len(df[df['change_type'] == 'Stable'])
        
        mean_nsm = df['nsm_pixels'].mean()
        std_nsm = df['nsm_pixels'].std()
        
        # Create summary figure
        fig = plt.figure(figsize=(12, 8))
        
        # Title
        fig.text(0.5, 0.95, 'PHASE 3 ANALYSIS SUMMARY STATISTICS', 
                ha='center', fontsize=16, fontweight='bold')
        
        # Statistics text
        stats_text = f"""
TRANSECT ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Transects Analyzed: {total_transects}

CHANGE CLASSIFICATION:
  • Erosion Zones:      {erosion_count} ({100*erosion_count/total_transects:.1f}%)
  • Accretion Zones:    {accretion_count} ({100*accretion_count/total_transects:.1f}%)
  • Stable Zones:       {stable_count} ({100*stable_count/total_transects:.1f}%)

SHORELINE MOVEMENT METRICS (1994-2024):
  • Mean NSM:           {mean_nsm:.2f} ± {std_nsm:.2f} pixels
  • Min NSM:            {df['nsm_pixels'].min():.2f} pixels
  • Max NSM:            {df['nsm_pixels'].max():.2f} pixels
  • Median NSM:         {df['nsm_pixels'].median():.2f} pixels

END POINT RATE (EPR):
  • Mean EPR:           {df['epr_pixels_per_year'].mean():.2f} pixels/year
  • Median EPR:         {df['epr_pixels_per_year'].median():.2f} pixels/year

MEAN ANNUAL CHANGE (MAC):
  • Mean MAC:           {df['mac_pixels_per_year'].mean():.2f} pixels/year
  • Median MAC:         {df['mac_pixels_per_year'].median():.2f} pixels/year

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        fig.text(0.1, 0.5, stats_text, 
                ha='left', va='center', fontsize=11, 
                family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.axis('off')
        
        output_file = Path(output_dir) / 'summary_statistics.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"✅ Saved: {output_file}")
        plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating summary statistics: {e}")
        return False


def main():
    """Generate all Phase 3 visualizations."""
    
    logger.info("=" * 80)
    logger.info("PHASE 3 VISUALIZATION - GENERATING PUBLICATION-READY PLOTS")
    logger.info("=" * 80)
    
    # Define directories
    analysis_dir = Path(project_root) / 'model_outputs' / 'analysis' / 'transects'
    forecast_dir = Path(project_root) / 'model_outputs' / 'analysis' / 'forecast'
    output_dir = Path(project_root) / 'model_outputs' / 'validation_plots'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Input: {analysis_dir}")
    logger.info(f"Output: {output_dir}\n")
    
    # Generate visualizations
    results = {
        'Erosion/Accretion Map': plot_erosion_accretion_map(analysis_dir, output_dir),
        'Change Metrics Distribution': plot_change_metrics(analysis_dir, output_dir),
        'LSTM Forecast Samples': plot_lstm_forecast(forecast_dir, output_dir),
        'Summary Statistics': plot_summary_statistics(analysis_dir, output_dir),
    }
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("VISUALIZATION RESULTS")
    logger.info("=" * 80)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        logger.info(f"{status} {name}")
    
    logger.info("\n" + "=" * 80)
    
    return all(results.values())


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
