#!/usr/bin/env python3
"""
Vector Export Main Script - Phase 2 GIS Output Generation

Executes the complete shoreline vector export pipeline:
  1. Reads all extracted shoreline coordinates from CSV files
  2. Creates spatial features with proper attributes
  3. Exports to three GIS-ready formats per year:
     - ESRI Shapefile
     - GeoJSON
     - KML
  4. Merges all years into combined datasets
  5. Generates validation plots

Run this script to generate GIS-ready shoreline vectors from the extraction phase.
"""

import sys
import os
from pathlib import Path

# Add utils to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.vector_export_utils import export_shorelines_to_vectors
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for vector export pipeline."""
    
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    processed_dir = project_root / 'model_outputs' / 'processed'
    
    if not processed_dir.exists():
        logger.error(f"Processed directory not found: {processed_dir}")
        return False
    
    logger.info(f"Project root: {project_root}")
    logger.info(f"Processing directory: {processed_dir}")
    logger.info(f"Output CRS: EPSG:4326 (WGS84)")
    
    # Run vector export
    outputs = export_shorelines_to_vectors(
        input_dir=str(processed_dir),
        output_dir=str(processed_dir),
        crs='EPSG:4326',
        years=[1994, 2004, 2014, 2024]
    )
    
    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("VECTOR EXPORT SUMMARY")
    logger.info("=" * 80)
    
    if not outputs:
        logger.error("No outputs generated")
        return False
    
    for year, formats in outputs.items():
        if formats:
            logger.info(f"\nYear {year}:")
            for fmt, filepath in formats.items():
                if os.path.exists(filepath):
                    size_kb = os.path.getsize(filepath) / 1024
                    logger.info(f"  ✓ {fmt:15} {filepath} ({size_kb:.1f} KB)")
                else:
                    logger.warning(f"  ✗ {fmt:15} FILE NOT FOUND")
    
    logger.info("\n" + "=" * 80)
    logger.info("Vector export complete!")
    logger.info("All files ready for GIS import (QGIS, ArcGIS, Google Earth)")
    logger.info("=" * 80)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
