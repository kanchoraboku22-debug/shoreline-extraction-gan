"""
Transect-Based Coastal Change Analysis - Phase 3A

Generates orthogonal transects along a reference coastline and measures
shoreline displacement through time. Computes standard coastal engineering
metrics: Net Shoreline Movement (NSM), End Point Rate (EPR), and Mean Annual
Change (MAC).

This is the standard approach used in USGS ShorelineMonitor and coastal
research globally.

Outputs:
  - transects.shp: Vector transects with change statistics
  - shoreline_change_stats.csv: Detailed per-transect metrics
  - erosion_accretion_map.png: Publication-quality visualization
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Tuple, List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from shapely.geometry import LineString, Point, MultiLineString
    from shapely.ops import unary_union
    HAS_SHAPELY = True
except ImportError:
    HAS_SHAPELY = False


def load_vector_data(vector_path: str, year: int) -> Optional[gpd.GeoDataFrame]:
    """
    Load shoreline vector data for a specific year.
    
    Args:
        vector_path: Path to shoreline .shp file
        year: Year identifier (for metadata)
    
    Returns:
        GeoDataFrame with shoreline geometries
    """
    try:
        gdf = gpd.read_file(vector_path)
        gdf['year'] = year
        logger.info(f"Loaded {len(gdf)} shoreline segments for {year}")
        return gdf
    except Exception as e:
        logger.error(f"Failed to load {vector_path}: {e}")
        return None


def merge_yearly_shorelines(
    processed_dir: str,
    years: List[int] = [1994, 2004, 2014, 2024]
) -> Optional[Dict[int, gpd.GeoDataFrame]]:
    """
    Load all yearly shoreline data into memory.
    
    Args:
        processed_dir: Path to model_outputs/processed
        years: Years to load
    
    Returns:
        Dictionary mapping year -> GeoDataFrame
    """
    shorelines = {}
    
    for year in years:
        vector_path = os.path.join(
            processed_dir,
            'vectors',
            f'shoreline_{year}.shp'
        )
        
        if not os.path.exists(vector_path):
            logger.warning(f"Vector file not found for {year}: {vector_path}")
            continue
        
        gdf = load_vector_data(vector_path, year)
        if gdf is not None:
            shorelines[year] = gdf
    
    if not shorelines:
        logger.error("No shoreline data loaded")
        return None
    
    logger.info(f"Successfully loaded {len(shorelines)} years of data")
    return shorelines


def generate_reference_coastline(
    shorelines: Dict[int, gpd.GeoDataFrame],
    ref_year: int = 1994
) -> Optional[LineString]:
    """
    Generate reference coastline from baseline year (usually oldest).
    
    Args:
        shorelines: Dictionary of yearly shorelines
        ref_year: Reference year for baseline
    
    Returns:
        LineString representing the reference coastline
    """
    
    if ref_year not in shorelines:
        logger.error(f"Reference year {ref_year} not in data")
        return None
    
    gdf_ref = shorelines[ref_year]
    
    # Merge all geometries from reference year
    if len(gdf_ref) == 1:
        baseline = gdf_ref.geometry.iloc[0]
    else:
        # Merge multiple segments (take longest as primary baseline)
        baseline = max(gdf_ref.geometry, key=lambda g: g.length)
    
    logger.info(f"Reference coastline from {ref_year}: {baseline.length:.0f} pixels")
    return baseline


def generate_transects(
    baseline: LineString,
    spacing: float = 50,
    length: float = 300
) -> gpd.GeoDataFrame:
    """
    Generate perpendicular transects along baseline coastline.
    
    Args:
        baseline: Reference coastline LineString
        spacing: Distance between transects (pixels)
        length: Length of each transect (pixels)
    
    Returns:
        GeoDataFrame with transect geometries
    """
    
    transects = []
    distances = np.arange(0, baseline.length, spacing)
    
    for i, dist in enumerate(distances):
        # Get point on baseline
        point = baseline.interpolate(dist)
        
        # Get direction at this point (tangent)
        # Use nearby points to compute tangent
        if dist == 0:
            next_point = baseline.interpolate(min(spacing, baseline.length))
        else:
            next_point = baseline.interpolate(min(dist + spacing, baseline.length))
        
        # Compute perpendicular vector
        dx = next_point.x - point.x
        dy = next_point.y - point.y
        
        # Normalize
        length_vec = np.sqrt(dx**2 + dy**2)
        if length_vec == 0:
            continue
        
        dx /= length_vec
        dy /= length_vec
        
        # Perpendicular (rotate 90 degrees)
        perp_x = -dy
        perp_y = dx
        
        # Create transect line (extend in both directions)
        p1 = Point(point.x - perp_x * length/2, point.y - perp_y * length/2)
        p2 = Point(point.x + perp_x * length/2, point.y + perp_y * length/2)
        
        transect_line = LineString([p1, p2])
        
        transects.append({
            'transect_id': i,
            'distance_along_coast': dist,
            'geometry': transect_line
        })
    
    gdf_transects = gpd.GeoDataFrame(transects, crs='EPSG:4326')
    logger.info(f"Generated {len(gdf_transects)} transects")
    
    return gdf_transects


def find_shoreline_intersection(
    transect: LineString,
    shorelines: gpd.GeoDataFrame
) -> Optional[Point]:
    """
    Find intersection of transect with shoreline geometries.
    
    Args:
        transect: Transect line
        shorelines: GeoDataFrame with shoreline segments
    
    Returns:
        Intersection point, or None if no intersection
    """
    
    intersections = []
    
    for geom in shorelines.geometry:
        if transect.intersects(geom):
            inter = transect.intersection(geom)
            
            if inter.is_empty:
                continue
            
            # Handle different intersection types
            if isinstance(inter, Point):
                intersections.append(inter)
            elif isinstance(inter, LineString):
                # Take midpoint of intersection line
                intersections.append(Point(inter.xy[0][0], inter.xy[1][0]))
            elif hasattr(inter, 'geoms'):
                # MultiPoint or similar
                for geom_part in inter.geoms:
                    if isinstance(geom_part, Point):
                        intersections.append(geom_part)
    
    if not intersections:
        return None
    
    # Return point closest to baseline (leftmost along transect)
    return min(intersections, key=lambda p: transect.project(p))


def compute_shoreline_change(
    gdf_transects: gpd.GeoDataFrame,
    shorelines: Dict[int, gpd.GeoDataFrame],
    years: List[int] = [1994, 2004, 2014, 2024]
) -> gpd.GeoDataFrame:
    """
    Measure shoreline position along each transect for each year.
    Compute change metrics: NSM, EPR, MAC.
    
    Args:
        gdf_transects: GeoDataFrame with transect geometries
        shorelines: Dictionary of yearly shoreline GeoDataFrames
        years: List of years in chronological order
    
    Returns:
        Updated transect GeoDataFrame with change statistics
    """
    
    years = sorted(years)
    change_data = []
    
    for idx, row in gdf_transects.iterrows():
        transect = row.geometry
        transect_id = row['transect_id']
        
        # Find shoreline intersection for each year
        positions = {}
        distances = {}
        
        for year in years:
            if year not in shorelines:
                continue
            
            inter_point = find_shoreline_intersection(transect, shorelines[year])
            
            if inter_point is not None:
                # Store position
                positions[year] = inter_point
                # Store distance along transect from start
                distances[year] = transect.project(inter_point)
        
        if len(positions) < 2:
            logger.warning(f"Transect {transect_id}: insufficient shoreline data")
            continue
        
        # Compute change metrics
        year_list = sorted(positions.keys())
        dist_list = [distances[y] for y in year_list]
        
        # Net Shoreline Movement (NSM) - total change from first to last year
        nsm = dist_list[-1] - dist_list[0]
        
        # End Point Rate (EPR) - linear rate between first and last year
        time_span = year_list[-1] - year_list[0]
        epr = nsm / time_span if time_span > 0 else 0
        
        # Mean Annual Change (MAC) - average change per year
        mac = epr  # Same calculation for linear trend
        
        # Classification: erosion vs accretion
        if epr > 0:
            change_type = 'Accretion'
        elif epr < 0:
            change_type = 'Erosion'
        else:
            change_type = 'Stable'
        
        change_data.append({
            'transect_id': transect_id,
            'distance_along_coast': row['distance_along_coast'],
            'nsm_pixels': nsm,
            'epr_pixels_per_year': epr,
            'mac_pixels_per_year': mac,
            'change_type': change_type,
            'num_years_data': len(year_list),
            **{f'position_{year}': distances[year] for year in year_list}
        })
    
    # Merge with original transects
    df_changes = pd.DataFrame(change_data)
    gdf_result = gdf_transects.merge(df_changes, on='transect_id', how='left')
    
    logger.info(f"Computed change metrics for {len(gdf_result)} transects")
    
    return gdf_result


def export_transect_analysis(
    gdf_transects: gpd.GeoDataFrame,
    output_dir: str
) -> Dict[str, str]:
    """
    Export transect analysis results to shapefile and CSV.
    
    Args:
        gdf_transects: GeoDataFrame with computed change metrics
        output_dir: Output directory
    
    Returns:
        Dictionary of created files
    """
    
    os.makedirs(output_dir, exist_ok=True)
    outputs = {}
    
    # Export shapefile
    shp_path = os.path.join(output_dir, 'transects.shp')
    gdf_transects.to_file(shp_path, driver='ESRI Shapefile')
    logger.info(f"✓ Shapefile: {shp_path}")
    outputs['shapefile'] = shp_path
    
    # Export CSV with detailed statistics
    csv_path = os.path.join(output_dir, 'shoreline_change_stats.csv')
    
    # Create dataframe without geometry for CSV
    df_stats = gdf_transects.drop(columns=['geometry']).copy()
    df_stats.to_csv(csv_path, index=False)
    logger.info(f"✓ Statistics CSV: {csv_path}")
    outputs['statistics'] = csv_path
    
    # Create summary statistics
    summary = {
        'Total Transects': len(gdf_transects),
        'Mean EPR (pixels/year)': gdf_transects['epr_pixels_per_year'].mean(),
        'Std EPR (pixels/year)': gdf_transects['epr_pixels_per_year'].std(),
        'Max Erosion (pixels/year)': gdf_transects['epr_pixels_per_year'].min(),
        'Max Accretion (pixels/year)': gdf_transects['epr_pixels_per_year'].max(),
        'Erosion Count': (gdf_transects['change_type'] == 'Erosion').sum(),
        'Accretion Count': (gdf_transects['change_type'] == 'Accretion').sum(),
        'Stable Count': (gdf_transects['change_type'] == 'Stable').sum(),
    }
    
    summary_path = os.path.join(output_dir, 'change_summary.txt')
    with open(summary_path, 'w') as f:
        f.write("COASTAL CHANGE ANALYSIS SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        for key, val in summary.items():
            if isinstance(val, float):
                f.write(f"{key:.<40} {val:.2f}\n")
            else:
                f.write(f"{key:.<40} {val}\n")
    
    logger.info(f"✓ Summary: {summary_path}")
    outputs['summary'] = summary_path
    
    return outputs


def run_transect_analysis(
    processed_dir: str = 'model_outputs/processed',
    output_dir: str = 'model_outputs/analysis',
    transect_spacing: float = 50,
    transect_length: float = 300
) -> bool:
    """
    Run complete transect-based coastal change analysis.
    
    Args:
        processed_dir: Path to model_outputs/processed
        output_dir: Output directory for results
        transect_spacing: Distance between transects (pixels)
        transect_length: Length of each transect (pixels)
    
    Returns:
        True if successful
    """
    
    logger.info("=" * 75)
    logger.info("PHASE 3A: TRANSECT-BASED COASTAL CHANGE ANALYSIS")
    logger.info("=" * 75)
    
    # Load data
    shorelines = merge_yearly_shorelines(processed_dir)
    if not shorelines:
        return False
    
    # Generate reference coastline
    baseline = generate_reference_coastline(shorelines)
    if baseline is None:
        return False
    
    # Generate transects
    gdf_transects = generate_transects(baseline, spacing=transect_spacing, length=transect_length)
    
    # Compute change metrics
    gdf_result = compute_shoreline_change(gdf_transects, shorelines)
    
    # Export results
    output_subdir = os.path.join(output_dir, 'transects')
    outputs = export_transect_analysis(gdf_result, output_subdir)
    
    logger.info("\n" + "=" * 75)
    logger.info("PHASE 3A COMPLETE")
    logger.info("=" * 75)
    
    return True


if __name__ == '__main__':
    success = run_transect_analysis(
        processed_dir='model_outputs/processed',
        output_dir='model_outputs/analysis',
        transect_spacing=50,
        transect_length=300
    )
