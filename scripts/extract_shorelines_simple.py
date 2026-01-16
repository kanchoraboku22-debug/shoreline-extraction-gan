"""
Simple shoreline extraction from segmentation masks.
Uses contour detection to extract shorelines without requiring geopandas.
"""
import os
import glob
import numpy as np
import cv2
import pandas as pd
from pathlib import Path

def extract_shoreline_from_mask(mask_path, tile_coords=None):
    """
    Extract shoreline contours from a binary segmentation mask.
    Returns list of (x, y) coordinates representing the shoreline.
    
    Args:
        mask_path: Path to binary segmentation mask image
        tile_coords: Tuple of (y, x) offsets if this is a tile
    
    Returns:
        List of contours, each as (x, y) coordinate arrays
    """
    # Read mask
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return []
    
    # Threshold if needed
    if mask.dtype != np.uint8 or mask.max() > 255:
        mask = cv2.normalize(mask, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Find contours using marching squares equivalent (edge detection)
    # Use morphological operations to clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    shorelines = []
    for contour in contours:
        # Filter by size - ignore very small contours (noise)
        if cv2.contourArea(contour) < 50:
            continue
        
        # Convert contour to coordinate list
        coords = contour.squeeze().astype(float)
        if len(coords.shape) == 1:  # Single point
            continue
        
        # Apply tile offset if this is from a tile
        if tile_coords is not None:
            coords[:, 0] += tile_coords[1]  # x offset
            coords[:, 1] += tile_coords[0]  # y offset
        
        shorelines.append(coords)
    
    return shorelines


def process_gan_outputs(gan_output_dir, coords_csv, site_name, output_dir):
    """
    Process all GAN output segmentation masks and extract shorelines.
    
    Args:
        gan_output_dir: Directory containing GAN output PNG masks
        coords_csv: CSV file with image metadata and coordinates
        site_name: Name of the site (e.g., 'Mombasa_2014')
        output_dir: Output directory for results
    """
    # Read coordinates metadata
    if os.path.exists(coords_csv):
        coords_df = pd.read_csv(coords_csv)
    else:
        print(f"[WARN] Coordinates CSV not found: {coords_csv}")
        coords_df = pd.DataFrame()
    
    # Create output subdirectories
    output_subdir = os.path.join(output_dir, 'processed', site_name)
    shorelines_dir = os.path.join(output_subdir, 'shorelines')
    images_dir = os.path.join(output_subdir, 'shoreline_images')
    kml_dir = os.path.join(output_subdir, 'kml_merged')
    shapefile_dir = os.path.join(output_subdir, 'shapefile_merged')
    
    for d in [shorelines_dir, images_dir, kml_dir, shapefile_dir]:
        os.makedirs(d, exist_ok=True)
    
    # Find all PNG masks
    mask_files = glob.glob(os.path.join(gan_output_dir, '*_fake_B.png'))
    print(f"[INFO] Found {len(mask_files)} segmentation masks")
    
    # Process each mask
    all_shorelines = []
    for mask_path in mask_files:
        basename = os.path.basename(mask_path)
        print(f"[INFO] Processing {basename}...")
        
        # Extract shorelines
        shorelines = extract_shoreline_from_mask(mask_path)
        
        # Save shoreline visualization
        img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
        for shoreline in shorelines:
            shoreline_int = shoreline.astype(np.int32)
            cv2.polylines(img_color, [shoreline_int], False, (0, 255, 0), 2)
        
        vis_path = os.path.join(images_dir, basename.replace('_fake_B.png', '_shoreline.png'))
        cv2.imwrite(vis_path, img_color)
        
        # Save shoreline data
        for i, shoreline in enumerate(shorelines):
            data_path = os.path.join(shorelines_dir, 
                                    basename.replace('_fake_B.png', f'_shoreline_{i}.txt'))
            np.savetxt(data_path, shoreline, fmt='%.6f', delimiter=',', 
                      header='x,y', comments='')
            all_shorelines.append({
                'file': basename,
                'shoreline_id': i,
                'num_points': len(shoreline),
                'path': data_path
            })
    
    # Save summary
    summary_df = pd.DataFrame(all_shorelines)
    summary_path = os.path.join(output_subdir, 'shorelines_summary.csv')
    summary_df.to_csv(summary_path, index=False)
    
    print(f"[OK] Extracted {len(all_shorelines)} shorelines")
    print(f"[OK] Results saved to {output_subdir}")
    
    return output_subdir


def main():
    """Extract shorelines from mock GAN outputs for all years."""
    base_output = os.path.join(os.getcwd(), 'model_outputs')
    gan_output_base = os.path.join(base_output, 'gan', 'shoreline_gan_mock', 'test_latest', 'images')
    years = [1994, 2004, 2014, 2024]
    
    for year in years:
        site = f'Mombasa_{year}'
        coords_csv = os.path.join('data', site, f'{site}.csv')
        
        print(f"\n[INFO] Extracting shorelines for {site}...")
        process_gan_outputs(gan_output_base, coords_csv, site, base_output)
    
    print("\n[SUCCESS] Shoreline extraction complete!")


if __name__ == '__main__':
    main()
