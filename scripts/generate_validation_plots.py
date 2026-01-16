"""
Validation Plots Generator - Publication-Ready Shoreline Visualization

Creates color-coded shoreline overlays for publication/presentation:
  - Overlay extracted shorelines on original satellite imagery
  - Color code by year (1994: Red, 2004: Orange, 2014: Green, 2024: Blue)
  - Generate high-quality PNG + SVG outputs

Suitable for thesis, journal papers, and conference presentations.
"""

import os
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import cv2
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import to_rgba
    HAS_VISUALIZATION = True
except ImportError:
    HAS_VISUALIZATION = False
    logger.warning("matplotlib/cv2 not available. Skipping visualization.")


# Define year color scheme for publication
YEAR_COLORS = {
    1994: '#FF0000',  # Red
    2004: '#FFA500',  # Orange
    2014: '#00AA00',  # Green
    2024: '#0055FF',  # Blue
}


def read_shoreline_coordinates(filepath: str) -> Optional[np.ndarray]:
    """
    Read shoreline coordinates from CSV file.
    
    Args:
        filepath: Path to coordinate CSV file
    
    Returns:
        NumPy array of shape (N, 2) with [x, y] coordinates
    """
    try:
        df = pd.read_csv(filepath)
        if not all(col in df.columns for col in ['x', 'y']):
            return None
        
        coords = df[['x', 'y']].values.astype(float)
        coords = coords[~np.isnan(coords).any(axis=1)]
        
        return coords if len(coords) >= 2 else None
    except:
        return None


def load_satellite_images_from_tiles(
    tile_dir: str
) -> Optional[np.ndarray]:
    """
    Load first satellite image tile for visualization.
    
    Args:
        tile_dir: Directory containing tile JPEGs
    
    Returns:
        Single tile image
    """
    try:
        tiles = sorted(glob.glob(os.path.join(tile_dir, '*.jpg')))
        
        if not tiles:
            return None
        
        # Load first tile
        tile = cv2.imread(tiles[0])
        if tile is None:
            return None
        
        return cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)
    except Exception as e:
        logger.warning(f"Failed to load tiles: {e}")
        return None


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple (0-255)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_shorelines_on_image(
    image: np.ndarray,
    shoreline_dir: str,
    year: int,
    thickness: int = 2,
    alpha: float = 0.7
) -> np.ndarray:
    """
    Draw extracted shorelines on satellite image.
    
    Args:
        image: Input RGB image (H, W, 3)
        shoreline_dir: Directory containing shoreline CSV files
        year: Year for color coding
        thickness: Line thickness in pixels
        alpha: Transparency blending factor
    
    Returns:
        Image with drawn shorelines
    """
    
    if image is None:
        return None
    
    output = image.copy().astype(float)
    color_hex = YEAR_COLORS.get(year, '#CCCCCC')
    color_rgb = hex_to_rgb(color_hex)
    
    # Load all shoreline files
    shoreline_files = sorted(glob.glob(os.path.join(shoreline_dir, '*_shoreline_*.txt')))
    
    count = 0
    for filepath in shoreline_files:
        coords = read_shoreline_coordinates(filepath)
        
        if coords is None:
            continue
        
        # Convert to integer pixel coordinates
        coords = coords.astype(np.int32)
        
        # Clip to image bounds
        h, w = image.shape[:2]
        coords = np.clip(coords, 0, [w-1, h-1])
        
        # Draw line
        if len(coords) > 1:
            for i in range(len(coords) - 1):
                pt1 = tuple(coords[i])
                pt2 = tuple(coords[i + 1])
                cv2.line(output, pt1, pt2, color_rgb, thickness)
                count += 1
    
    # Blend with original
    output = (alpha * output + (1 - alpha) * image.astype(float))
    output = np.clip(output, 0, 255).astype(np.uint8)
    
    logger.info(f"Drew {count} line segments for year {year}")
    return output


def create_multi_year_comparison(
    project_dir: str,
    processed_dir: str,
    output_path: str,
    dpi: int = 150
) -> bool:
    """
    Create 2x2 subplot showing all years with color-coded shorelines.
    
    Args:
        project_dir: Path to project root
        processed_dir: Path to model_outputs/processed
        output_path: Path to save PNG image
        dpi: Resolution for saved image
    
    Returns:
        True if successful
    """
    
    if not HAS_VISUALIZATION:
        logger.warning("Visualization libraries not available")
        return False
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Mombasa Shoreline Extraction - 1994 to 2024', fontsize=16, fontweight='bold')
    
    years = [1994, 2004, 2014, 2024]
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for year, (row, col) in zip(years, positions):
        ax = axes[row, col]
        
        # Load composite from tiles
        tile_dir = os.path.join(
            project_dir,
            'data',
            f'Mombasa_{year}',
            'jpg_files',
            'preprocessed'
        )
        
        img = load_satellite_images_from_tiles(tile_dir)
        
        if img is not None:
            # Draw shorelines
            shoreline_dir = os.path.join(processed_dir, f'Mombasa_{year}', 'shorelines')
            img_with_shorelines = draw_shorelines_on_image(
                img,
                shoreline_dir,
                year,
                thickness=2,
                alpha=0.6
            )
            
            ax.imshow(img_with_shorelines)
            ax.set_title(f'{year}', fontsize=12, fontweight='bold')
        else:
            logger.warning(f"Could not load images for year {year}")
            ax.text(0.5, 0.5, f'Images not found\n({year})', 
                   ha='center', va='center', fontsize=12)
        
        ax.axis('off')
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=YEAR_COLORS[1994], label='1994 - Red'),
        mpatches.Patch(facecolor=YEAR_COLORS[2004], label='2004 - Orange'),
        mpatches.Patch(facecolor=YEAR_COLORS[2014], label='2014 - Green'),
        mpatches.Patch(facecolor=YEAR_COLORS[2024], label='2024 - Blue'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10)
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    try:
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.info(f"✓ Saved multi-year comparison: {output_path}")
        plt.close()
        return True
    except Exception as e:
        logger.error(f"Failed to save figure: {e}")
        return False


def create_single_year_overlay(
    project_dir: str,
    processed_dir: str,
    year: int,
    output_dir: str,
    dpi: int = 150
) -> Optional[str]:
    """
    Create high-quality overlay of shorelines on satellite image.
    
    Args:
        project_dir: Path to project root
        processed_dir: Path to model_outputs/processed
        year: Year to process
        output_dir: Directory to save output
        dpi: Resolution for saved image
    
    Returns:
        Path to saved image, or None if failed
    """
    
    if not HAS_VISUALIZATION:
        return None
    
    # Load composite from tiles
    tile_dir = os.path.join(
        project_dir,
        'data',
        f'Mombasa_{year}',
        'jpg_files',
        'preprocessed'
    )
    
    img = load_satellite_images_from_tiles(tile_dir)
    if img is None:
        logger.warning(f"Could not load images for year {year}")
        return None
    
    # Draw shorelines
    shoreline_dir = os.path.join(processed_dir, f'Mombasa_{year}', 'shorelines')
    img_with_shorelines = draw_shorelines_on_image(
        img,
        shoreline_dir,
        year,
        thickness=2,
        alpha=0.5
    )
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10), dpi=dpi)
    ax.imshow(img_with_shorelines)
    ax.set_title(f'Mombasa Shorelines - {year}', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Add colorbar info
    color_hex = YEAR_COLORS[year]
    ax.text(0.02, 0.98, f'Shoreline Color: {color_hex}', 
           transform=ax.transAxes, fontsize=10,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Save
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'shoreline_overlay_{year}.png')
    
    try:
        plt.tight_layout()
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.info(f"✓ Saved overlay: {output_path}")
        plt.close()
        return output_path
    except Exception as e:
        logger.error(f"Failed to save overlay: {e}")
        return None


def generate_validation_plots(
    project_dir: str = '.',
    processed_dir: str = 'model_outputs/processed',
    output_dir: str = 'model_outputs/validation_plots'
) -> Dict[str, str]:
    """
    Generate all validation plots.
    
    Args:
        project_dir: Path to project root
        processed_dir: Path to model_outputs/processed
        output_dir: Directory to save plots
    
    Returns:
        Dictionary of created files
    """
    
    if not HAS_VISUALIZATION:
        logger.error("matplotlib/cv2 required for visualization")
        return {}
    
    logger.info("=" * 80)
    logger.info("VALIDATION PLOTS GENERATION - Starting")
    logger.info("=" * 80)
    
    os.makedirs(output_dir, exist_ok=True)
    outputs = {}
    
    # Create multi-year comparison
    comparison_path = os.path.join(output_dir, 'shoreline_comparison_all_years.png')
    if create_multi_year_comparison(project_dir, processed_dir, comparison_path):
        outputs['comparison'] = comparison_path
    
    # Create per-year overlays
    for year in [1994, 2004, 2014, 2024]:
        overlay_path = create_single_year_overlay(project_dir, processed_dir, year, output_dir)
        if overlay_path:
            outputs[f'overlay_{year}'] = overlay_path
    
    logger.info("\n" + "=" * 80)
    logger.info("VALIDATION PLOTS - Complete")
    logger.info("=" * 80)
    
    return outputs


if __name__ == '__main__':
    from pathlib import Path
    project_root = Path.cwd()
    
    outputs = generate_validation_plots(
        project_dir=str(project_root),
        processed_dir='model_outputs/processed',
        output_dir='model_outputs/validation_plots'
    )
    
    print("\nGenerated plots:")
    for key, path in outputs.items():
        print(f"  {key}: {path}")
