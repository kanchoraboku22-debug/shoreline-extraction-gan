"""
Vector Export Utilities for Shoreline GAN Project

Converts extracted shoreline coordinates (CSV format) into GIS-ready vector formats:
  - ESRI Shapefile (.shp)
  - GeoJSON (.geojson)
  - Google Earth KML (.kml)

All outputs are WGS84 (EPSG:4326) for web/GIS compatibility.

Usage:
    from utils.vector_export_utils import export_shorelines_to_vectors
    
    export_shorelines_to_vectors(
        input_dir='model_outputs/processed',
        output_dir='model_outputs/processed',
        crs='EPSG:4326'
    )
"""

import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import geopandas as gpd
    from shapely.geometry import LineString, Point, MultiLineString
    from shapely.ops import unary_union
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False
    logger.warning("geopandas not installed. Vector export will be skipped.")


def _create_kml_from_geojson(geojson_dict: dict, year: int) -> str:
    """
    Convert GeoJSON to KML format for Google Earth compatibility.
    
    Args:
        geojson_dict: GeoJSON feature collection dictionary
        year: Year identifier for styling
    
    Returns:
        KML XML string
    """
    
    kml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Shoreline {year}</name>
    <description>Extracted shorelines for year {year}</description>
    <Style id="shoreline-style">
      <LineStyle>
        <color>ff0055FF</color>
        <width>2</width>
      </LineStyle>
    </Style>
    {placemarks}
  </Document>
</kml>'''
    
    placemarks = []
    features = geojson_dict.get('features', [])
    
    for feat in features:
        try:
            coords = feat.get('geometry', {}).get('coordinates', [])
            props = feat.get('properties', {})
            
            if not coords:
                continue
            
            # Build coordinate string
            coord_str = '\n                '.join(
                [f"{lon},{lat},0" for lon, lat in coords]
            )
            
            segment_id = props.get('segment_id', 'unknown')
            length = props.get('length_m', 0)
            
            placemark = f'''    <Placemark>
      <name>Segment {segment_id}</name>
      <description>
        Year: {year}
        Length: {length:.1f} pixels
        Segment ID: {segment_id}
      </description>
      <styleUrl>#shoreline-style</styleUrl>
      <LineString>
        <coordinates>
                {coord_str}
        </coordinates>
      </LineString>
    </Placemark>'''
            
            placemarks.append(placemark)
        except:
            pass
    
    kml_content = kml_template.format(
        year=year,
        placemarks='\n'.join(placemarks)
    )
    
    return kml_content


def read_shoreline_coordinates(filepath: str) -> Optional[np.ndarray]:
    """
    Read shoreline coordinates from CSV file.
    
    Expected format:
        x,y
        1.0,85.0
        0.0,86.0
        ...
    
    Args:
        filepath: Path to coordinate CSV file
    
    Returns:
        NumPy array of shape (N, 2) with [x, y] coordinates, or None if invalid
    """
    try:
        df = pd.read_csv(filepath)
        
        # Validate columns
        if not all(col in df.columns for col in ['x', 'y']):
            logger.warning(f"Invalid columns in {filepath}: {df.columns.tolist()}")
            return None
        
        # Extract coordinates
        coords = df[['x', 'y']].values.astype(float)
        
        # Filter out NaN values
        coords = coords[~np.isnan(coords).any(axis=1)]
        
        if len(coords) < 2:
            logger.warning(f"Insufficient coordinates in {filepath}: {len(coords)} points")
            return None
        
        return coords
    
    except Exception as e:
        logger.warning(f"Error reading {filepath}: {e}")
        return None


def extract_year_from_filename(filename: str) -> Optional[int]:
    """
    Extract year from shoreline filename.
    
    Examples:
        'mombasa_1994_RGB_0000_0000_shoreline_0.txt' -> 1994
        'mombasa_2024_RGB_0512_1024_shoreline_5.txt' -> 2024
    """
    parts = filename.split('_')
    for part in parts:
        if part.isdigit() and len(part) == 4 and part.startswith('19') or part.startswith('20'):
            try:
                year = int(part)
                if 1990 <= year <= 2030:
                    return year
            except:
                pass
    return None


def extract_tile_coords_from_filename(filename: str) -> Tuple[int, int]:
    """
    Extract tile coordinates from shoreline filename.
    
    Filename format: mombasa_YYYY_RGB_XXXX_YYYY_shoreline_N.txt
    Returns: (x_offset, y_offset)
    
    Example:
        'mombasa_1994_RGB_0256_0512_shoreline_3.txt' -> (256, 512)
    """
    try:
        parts = filename.split('_')
        # Pattern: mombasa | YYYY | RGB | XXXX | YYYY | shoreline | N.txt
        if len(parts) >= 5:
            x_offset = int(parts[3])
            y_offset = int(parts[4])
            return (x_offset, y_offset)
    except:
        pass
    return (0, 0)


def create_geospatial_features(
    shorelines_dir: str,
    year: int,
    crs: str = 'EPSG:4326'
) -> Optional[gpd.GeoDataFrame]:
    """
    Create GeoDataFrame from all shoreline files in a year directory.
    
    Args:
        shorelines_dir: Path to directory containing coordinate CSV files
        year: Year for this batch of shorelines
        crs: Coordinate Reference System (default: WGS84)
    
    Returns:
        GeoDataFrame with LineString geometries and attributes
    """
    
    if not HAS_GEOPANDAS:
        logger.error("geopandas required for vector export")
        return None
    
    shoreline_files = glob.glob(os.path.join(shorelines_dir, '*_shoreline_*.txt'))
    
    if not shoreline_files:
        logger.warning(f"No shoreline files found in {shorelines_dir}")
        return None
    
    features = []
    segment_id = 0
    
    for filepath in sorted(shoreline_files):
        coords = read_shoreline_coordinates(filepath)
        
        if coords is None or len(coords) < 2:
            continue
        
        # Create LineString
        try:
            line = LineString(coords)
        except:
            logger.warning(f"Failed to create LineString from {filepath}")
            continue
        
        # Skip invalid geometries
        if not line.is_valid or line.length == 0:
            logger.warning(f"Invalid geometry in {filepath}")
            continue
        
        # Extract metadata
        filename = os.path.basename(filepath)
        tile_x, tile_y = extract_tile_coords_from_filename(filename)
        
        features.append({
            'geometry': line,
            'year': year,
            'segment_id': segment_id,
            'source_tile': filename,
            'length_m': line.length,  # Pixel units (will be actual meters if CRS proj)
            'num_points': len(coords),
            'tile_x': tile_x,
            'tile_y': tile_y
        })
        
        segment_id += 1
    
    if not features:
        logger.warning(f"No valid features created from {shorelines_dir}")
        return None
    
    gdf = gpd.GeoDataFrame(features, crs=crs)
    logger.info(f"Year {year}: Created {len(gdf)} shoreline features")
    
    return gdf


def export_year_vectors(
    year: int,
    year_dir: str,
    output_dir: str,
    crs: str = 'EPSG:4326'
) -> Dict[str, str]:
    """
    Export all shorelines for a single year to multiple vector formats.
    
    Args:
        year: Year identifier
        year_dir: Path to Mombasa_YYYY directory
        output_dir: Directory to write vector outputs
        crs: Coordinate Reference System
    
    Returns:
        Dictionary with paths to created files
    """
    
    if not HAS_GEOPANDAS:
        return {}
    
    shorelines_dir = os.path.join(year_dir, 'shorelines')
    
    if not os.path.isdir(shorelines_dir):
        logger.warning(f"Shorelines directory not found: {shorelines_dir}")
        return {}
    
    # Create GeoDataFrame
    gdf = create_geospatial_features(shorelines_dir, year, crs)
    
    if gdf is None or len(gdf) == 0:
        logger.warning(f"No features for year {year}")
        return {}
    
    # Create output directory
    vectors_dir = os.path.join(output_dir, 'vectors')
    os.makedirs(vectors_dir, exist_ok=True)
    
    # Define output filenames
    base_name = f'shoreline_{year}'
    shp_path = os.path.join(vectors_dir, f'{base_name}.shp')
    geojson_path = os.path.join(vectors_dir, f'{base_name}.geojson')
    kml_path = os.path.join(vectors_dir, f'{base_name}.kml')
    
    outputs = {}
    
    try:
        # Export Shapefile
        gdf.to_file(shp_path, driver='ESRI Shapefile')
        logger.info(f"✓ Shapefile: {shp_path}")
        outputs['shapefile'] = shp_path
    except Exception as e:
        logger.error(f"Failed to export shapefile: {e}")
    
    try:
        # Export GeoJSON
        gdf.to_file(geojson_path, driver='GeoJSON')
        logger.info(f"✓ GeoJSON: {geojson_path}")
        outputs['geojson'] = geojson_path
    except Exception as e:
        logger.error(f"Failed to export GeoJSON: {e}")
    
    try:
        # Export KML (convert GeoJSON to KML via intermediate format)
        geojson_dict = gdf.to_json()
        import json
        kml_content = _create_kml_from_geojson(json.loads(geojson_dict), year)
        with open(kml_path, 'w') as f:
            f.write(kml_content)
        logger.info(f"✓ KML: {kml_path}")
        outputs['kml'] = kml_path
    except Exception as e:
        logger.warning(f"Failed to export KML: {e}")
    
    return outputs


def merge_all_years(
    processed_dir: str,
    output_dir: str,
    years: List[int] = [1994, 2004, 2014, 2024],
    crs: str = 'EPSG:4326'
) -> Dict[str, str]:
    """
    Merge shorelines from all years into combined GIS datasets.
    
    Args:
        processed_dir: Path to model_outputs/processed directory
        output_dir: Output directory for merged vectors
        years: List of years to process
        crs: Coordinate Reference System
    
    Returns:
        Dictionary with paths to merged vector files
    """
    
    if not HAS_GEOPANDAS:
        return {}
    
    all_gdfs = []
    
    for year in years:
        year_dir = os.path.join(processed_dir, f'Mombasa_{year}')
        
        if not os.path.isdir(year_dir):
            logger.warning(f"Year directory not found: {year_dir}")
            continue
        
        shorelines_dir = os.path.join(year_dir, 'shorelines')
        gdf = create_geospatial_features(shorelines_dir, year, crs)
        
        if gdf is not None and len(gdf) > 0:
            all_gdfs.append(gdf)
    
    if not all_gdfs:
        logger.warning("No GeoDataFrames to merge")
        return {}
    
    # Merge all years
    merged_gdf = pd.concat(all_gdfs, ignore_index=True)
    logger.info(f"Merged {len(merged_gdf)} total features across all years")
    
    # Create output directory for combined datasets
    combined_dir = os.path.join(output_dir, 'combined')
    os.makedirs(combined_dir, exist_ok=True)
    
    outputs = {}
    
    try:
        # Shapefile
        merged_shp = os.path.join(combined_dir, 'shoreline_all_years.shp')
        merged_gdf.to_file(merged_shp, driver='ESRI Shapefile')
        logger.info(f"✓ Combined Shapefile: {merged_shp}")
        outputs['shapefile'] = merged_shp
    except Exception as e:
        logger.error(f"Failed to export merged shapefile: {e}")
    
    try:
        # GeoJSON
        merged_geojson = os.path.join(combined_dir, 'shoreline_all_years.geojson')
        merged_gdf.to_file(merged_geojson, driver='GeoJSON')
        logger.info(f"✓ Combined GeoJSON: {merged_geojson}")
        outputs['geojson'] = merged_geojson
    except Exception as e:
        logger.error(f"Failed to export merged GeoJSON: {e}")
    
    try:
        # KML
        geojson_dict = merged_gdf.to_json()
        import json
        kml_content = _create_kml_from_geojson(json.loads(geojson_dict), 'all_years')
        merged_kml = os.path.join(combined_dir, 'shoreline_all_years.kml')
        with open(merged_kml, 'w') as f:
            f.write(kml_content)
        logger.info(f"✓ Combined KML: {merged_kml}")
        outputs['kml'] = merged_kml
    except Exception as e:
        logger.warning(f"Failed to export merged KML: {e}")
    
    return outputs


def export_shorelines_to_vectors(
    input_dir: str = 'model_outputs/processed',
    output_dir: str = 'model_outputs/processed',
    crs: str = 'EPSG:4326',
    years: List[int] = [1994, 2004, 2014, 2024]
) -> Dict[int, Dict[str, str]]:
    """
    Main entry point: Export all shorelines to GIS-ready vector formats.
    
    Creates per-year and combined multi-year datasets in three formats:
      - ESRI Shapefile (.shp + .dbf + .shx + .prj)
      - GeoJSON (.geojson)
      - KML (.kml)
    
    All outputs use WGS84 (EPSG:4326) for GIS/web compatibility.
    
    Args:
        input_dir: Path to model_outputs/processed directory
        output_dir: Path to output directory (typically same as input)
        crs: Coordinate Reference System (default: WGS84)
        years: List of years to process (default: [1994, 2004, 2014, 2024])
    
    Returns:
        Dictionary mapping year -> {format -> filepath}
    
    Example:
        outputs = export_shorelines_to_vectors(
            input_dir='model_outputs/processed',
            output_dir='model_outputs/processed',
            crs='EPSG:4326'
        )
        # outputs = {
        #     1994: {'shapefile': '...', 'geojson': '...', 'kml': '...'},
        #     2004: {...},
        #     ...
        # }
    """
    
    if not HAS_GEOPANDAS:
        logger.error("geopandas is required. Install with: pip install geopandas")
        return {}
    
    logger.info("=" * 80)
    logger.info("SHORELINE VECTOR EXPORT - Starting")
    logger.info("=" * 80)
    
    output_summary = {}
    
    # Export per-year vectors
    for year in years:
        year_dir = os.path.join(input_dir, f'Mombasa_{year}')
        
        if not os.path.isdir(year_dir):
            logger.warning(f"Skipping year {year}: directory not found")
            continue
        
        logger.info(f"\nProcessing year {year}...")
        outputs = export_year_vectors(year, year_dir, output_dir, crs)
        output_summary[year] = outputs
    
    # Export merged multi-year dataset
    logger.info("\nMerging all years...")
    merged_outputs = merge_all_years(input_dir, output_dir, years, crs)
    output_summary['all_years'] = merged_outputs
    
    logger.info("\n" + "=" * 80)
    logger.info("VECTOR EXPORT - Complete")
    logger.info("=" * 80)
    
    return output_summary


if __name__ == '__main__':
    # Example usage
    outputs = export_shorelines_to_vectors(
        input_dir='model_outputs/processed',
        output_dir='model_outputs/processed',
        crs='EPSG:4326'
    )
    
    print("\n\nSummary of created files:")
    for key, val in outputs.items():
        print(f"\n{key}:")
        if isinstance(val, dict):
            for fmt, path in val.items():
                print(f"  {fmt}: {path}")
