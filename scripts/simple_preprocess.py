"""
Simple preprocessing script that converts RGB TIFs to JPEGs and creates pix2pix splits.
Works around ctypes/rasterio issues by using OpenCV directly.
"""
import os
import glob
import numpy as np
import cv2
from pathlib import Path

BASE = 'data'
YEARS = [1994, 2004, 2014, 2024]

def load_tif_with_opencv(tif_path):
    """Load TIF file using OpenCV (works with BGR/RGB TIFs)."""
    # Try using OpenCV's imreadmulti for multi-band TIFs
    try:
        # For simple RGB TIFs, imread should work
        img = cv2.imread(tif_path, cv2.IMREAD_COLOR)
        if img is None:
            # Try reading as is without color conversion
            img = cv2.imread(tif_path, cv2.IMREAD_UNCHANGED)
        return img
    except Exception as e:
        print(f"Warning: Could not load {tif_path} with OpenCV: {e}")
        return None

def scale_to_uint8(data):
    """Normalize data to 0-255 uint8 range."""
    if data is None or len(data) == 0:
        return np.zeros_like(data, dtype='uint8')
    
    data = np.asarray(data, dtype='float32')
    # Handle NaNs and infinities
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Use percentile-based normalization for robustness
    p2 = np.nanpercentile(data, 2)
    p98 = np.nanpercentile(data, 98)
    
    if p98 - p2 <= 0:
        return np.zeros_like(data, dtype='uint8')
    
    scaled = 255.0 * (data - p2) / (p98 - p2)
    scaled = np.clip(scaled, 0, 255).astype('uint8')
    return scaled

def process_rgb_tif_to_jpg(tif_path, output_jpg_path, output_jpeg_path=None):
    """Convert RGB TIF to JPEG and optionally to .jpeg."""
    img = load_tif_with_opencv(tif_path)
    if img is None:
        return False
    
    # If already 3-channel, use it directly
    if len(img.shape) == 3 and img.shape[2] >= 3:
        rgb = img[:, :, :3]
    elif len(img.shape) == 2:
        # Grayscale - replicate to 3 channels
        rgb = np.stack([img, img, img], axis=2)
    else:
        print(f"Unexpected image shape: {img.shape}")
        return False
    
    # Normalize each channel
    rgb_u8 = np.zeros_like(rgb, dtype='uint8')
    for b in range(min(3, rgb.shape[2])):
        rgb_u8[:, :, b] = scale_to_uint8(rgb[:, :, b])
    
    # Save as JPG
    os.makedirs(os.path.dirname(output_jpg_path), exist_ok=True)
    cv2.imwrite(output_jpg_path, rgb_u8)
    
    # Also save as .jpeg if requested (for GAN inference)
    if output_jpeg_path:
        os.makedirs(os.path.dirname(output_jpeg_path), exist_ok=True)
        cv2.imwrite(output_jpeg_path, rgb_u8)
    
    return True

def split_and_resize_simple(input_dir, output_dir, tile_size=256, overlap=0, use_jpeg=False):
    """
    Split large images into 256x256 tiles for pix2pix training.
    If use_jpeg=True, saves as .jpeg instead of .jpg
    """
    os.makedirs(output_dir, exist_ok=True)
    
    jpg_files = glob.glob(os.path.join(input_dir, '*.jpg'))
    print(f"Found {len(jpg_files)} JPEGs to process")
    
    tile_count = 0
    for jpg_path in jpg_files:
        img = cv2.imread(jpg_path)
        if img is None:
            print(f"Could not read {jpg_path}")
            continue
        
        h, w = img.shape[:2]
        basename = os.path.splitext(os.path.basename(jpg_path))[0]
        
        # Create tiles
        for y in range(0, h - tile_size + 1, tile_size - overlap):
            for x in range(0, w - tile_size + 1, tile_size - overlap):
                tile = img[y:y+tile_size, x:x+tile_size]
                if tile.shape[0] == tile_size and tile.shape[1] == tile_size:
                    ext = '.jpeg' if use_jpeg else '.jpg'
                    tile_name = f"{basename}_{y:04d}_{x:04d}{ext}"
                    tile_path = os.path.join(output_dir, tile_name)
                    cv2.imwrite(tile_path, tile)
                    tile_count += 1
    
    print(f"Created {tile_count} tiles in {output_dir}")
    return tile_count

def main():
    """Process all Mombasa years."""
    for year in YEARS:
        site = f'Mombasa_{year}'
        site_folder = os.path.join(BASE, site)
        
        if not os.path.exists(site_folder):
            print(f"[SKIP] {site_folder} does not exist")
            continue
        
        # Step 1: Convert RGB TIF to JPEG
        tif_path = os.path.join(site_folder, f'mombasa_{year}_RGB.tif')
        jpg_path = os.path.join(site_folder, 'jpg_files', 'preprocessed', f'mombasa_{year}_RGB.jpg')
        jpeg_path = os.path.join(site_folder, 'jpg_files', 'preprocessed', f'mombasa_{year}_RGB.jpeg')
        
        if not os.path.exists(tif_path):
            print(f"[SKIP] TIF not found: {tif_path}")
            continue
        
        print(f"[INFO] Converting {tif_path} to JPEG...")
        if process_rgb_tif_to_jpg(tif_path, jpg_path, jpeg_path):
            print(f"[OK] Saved JPEG to {jpg_path}")
        else:
            print(f"[ERROR] Could not convert TIF for {site}")
            continue
        
        # Step 2: Create pix2pix tiles (.jpeg format for GAN inference)
        preprocessed_dir = os.path.join(site_folder, 'jpg_files', 'preprocessed')
        pix2pix_dir = os.path.join(site_folder, 'jpg_files', 'pix2pix_ready')
        
        print(f"[INFO] Creating pix2pix tiles for {site}...")
        split_and_resize_simple(preprocessed_dir, pix2pix_dir, tile_size=256, overlap=0, use_jpeg=True)
    
    print("[SUCCESS] Preprocessing complete!")

if __name__ == '__main__':
    main()
