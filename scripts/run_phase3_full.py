#!/usr/bin/env python3
"""
PHASE 3 ORCHESTRATION - Full Temporal Change & Forecasting Pipeline

Executes all three Phase 3 components in sequence:
  1. Phase 3A: Transect-based coastal change analysis
  2. Phase 3B: Time-series assembly for LSTM
  3. Phase 3C: LSTM model training and shoreline forecasting

Run this script to generate the complete temporal analysis and predictions.
"""

import sys
import os
from pathlib import Path
import logging

# Add utils to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.transect_analysis import run_transect_analysis
from utils.timeseries_assembly import assemble_timeseries
from utils.lstm_forecasting import run_lstm_forecasting

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Execute complete Phase 3 pipeline."""
    
    logger.info("=" * 80)
    logger.info("PHASE 3: TEMPORAL CHANGE & FORECASTING - LAUNCHING")
    logger.info("=" * 80)
    
    # Define directories
    processed_dir = project_root / 'model_outputs' / 'processed'
    analysis_dir = project_root / 'model_outputs' / 'analysis'
    
    if not processed_dir.exists():
        logger.error(f"Processed directory not found: {processed_dir}")
        return False
    
    logger.info(f"\nProject root: {project_root}")
    logger.info(f"Input (Phase 2): {processed_dir}")
    logger.info(f"Output: {analysis_dir}")
    
    # PHASE 3A: Transect Analysis
    logger.info("\n" + "=" * 80)
    logger.info("EXECUTING PHASE 3A: TRANSECT-BASED COASTAL CHANGE ANALYSIS")
    logger.info("=" * 80)
    
    success_3a = run_transect_analysis(
        processed_dir=str(processed_dir),
        output_dir=str(analysis_dir),
        transect_spacing=50,
        transect_length=300
    )
    
    if not success_3a:
        logger.error("Phase 3A failed")
        return False
    
    logger.info("✅ Phase 3A complete")
    
    # PHASE 3B: Time-Series Assembly
    logger.info("\n" + "=" * 80)
    logger.info("EXECUTING PHASE 3B: TIME-SERIES ASSEMBLY FOR LSTM")
    logger.info("=" * 80)
    
    transects_dir = analysis_dir / 'transects'
    timeseries_dir = analysis_dir / 'timeseries'
    
    success_3b = assemble_timeseries(
        analysis_dir=str(transects_dir),
        output_dir=str(timeseries_dir)
    )
    
    if not success_3b:
        logger.error("Phase 3B failed")
        return False
    
    logger.info("✅ Phase 3B complete")
    
    # PHASE 3C: LSTM Forecasting
    logger.info("\n" + "=" * 80)
    logger.info("EXECUTING PHASE 3C: LSTM FORECASTING")
    logger.info("=" * 80)
    
    forecast_dir = analysis_dir / 'forecast'
    
    success_3c = run_lstm_forecasting(
        timeseries_dir=str(timeseries_dir),
        output_dir=str(forecast_dir),
        epochs=50
    )
    
    if not success_3c:
        logger.error("Phase 3C failed")
        return False
    
    logger.info("✅ Phase 3C complete")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("PHASE 3 COMPLETE - ALL COMPONENTS SUCCESSFUL")
    logger.info("=" * 80)
    logger.info(f"\nOutputs generated in: {analysis_dir}")
    logger.info("\nDirectory structure:")
    logger.info(f"  {analysis_dir}/transects/       → Phase 3A results")
    logger.info(f"  {analysis_dir}/timeseries/      → Phase 3B results")
    logger.info(f"  {analysis_dir}/forecast/        → Phase 3C results")
    logger.info("\n" + "=" * 80)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
