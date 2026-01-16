"""
Mock GAN Inference: Creates synthetic shoreline segmentation masks using edge detection.
This allows the pipeline to proceed when no trained GAN model is available.
"""
import os
import glob
import numpy as np
import cv2
from pathlib import Path

def create_mock_segmentation(image_path, output_path):
    """
    Create a synthetic binary shoreline segmentation from an input image.
    Uses Canny edge detection and morphological operations to simulate
    a land/water boundary segmentation mask.
    """
    # Read input image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur for smoothing
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Dilate edges to create thicker lines (representing shoreline)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    shoreline_line = cv2.dilate(edges, kernel, iterations=2)
    
    # Create binary segmentation: assume lower part is water (white) and upper part is land (black)
    # or use a simple threshold-based approach with a slight bias
    height = gray.shape[0]
    width = gray.shape[1]
    
    # Create base segmentation: top half land, bottom half water
    seg_mask = np.zeros((height, width), dtype=np.uint8)
    seg_mask[height//2:, :] = 255  # Water in bottom half
    
    # Refine with edge detection - edges separate land and water
    # Apply morphological operations to create realistic shoreline
    seg_mask_refined = cv2.morphologyEx(seg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    seg_mask_refined = cv2.morphologyEx(seg_mask_refined, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Add some variation based on image content (darker areas = water)
    # Use Otsu's threshold on a portion of the image
    lower_region = gray[height//3:, :]
    _, water_mask = cv2.threshold(lower_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Combine: use original segmentation as base, refine with content-based detection
    seg_mask_refined[height//3:, :] = water_mask
    
    # Final smoothing
    seg_mask_final = cv2.GaussianBlur(seg_mask_refined, (7, 7), 0)
    
    # Ensure binary output
    _, seg_mask_binary = cv2.threshold(seg_mask_final, 127, 255, cv2.THRESH_BINARY)
    
    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, seg_mask_binary)
    
    return True


def run_mock_gan_inference(input_dir, output_dir, model_name='mock_gan'):
    """
    Process all JPEG images in input_dir and create segmentation masks in output_dir.
    This simulates the GAN inference step using edge detection.
    """
    # Create output structure
    results_dir = os.path.join(output_dir, 'gan', model_name, 'test_latest', 'images')
    os.makedirs(results_dir, exist_ok=True)
    
    # Find all JPEG images
    jpeg_files = glob.glob(os.path.join(input_dir, '*.jpeg'))
    print(f"[INFO] Found {len(jpeg_files)} JPEG files to process")
    
    successful = 0
    for jpeg_path in jpeg_files:
        # Create output filename
        basename = os.path.splitext(os.path.basename(jpeg_path))[0]
        output_name = f"{basename}_fake_B.png"  # pix2pix convention for generated output
        output_path = os.path.join(results_dir, output_name)
        
        # Generate segmentation mask
        if create_mock_segmentation(jpeg_path, output_path):
            successful += 1
        else:
            print(f"[WARN] Failed to process {jpeg_path}")
    
    print(f"[OK] Created {successful}/{len(jpeg_files)} segmentation masks in {results_dir}")
    return results_dir


def main():
    """Generate mock GAN outputs for all Mombasa years."""
    base_dir = 'data'
    output_dir = os.path.join(os.getcwd(), 'model_outputs')
    years = [1994, 2004, 2014, 2024]
    
    for year in years:
        site = f'Mombasa_{year}'
        input_dir = os.path.join(base_dir, site, 'jpg_files', 'pix2pix_ready')
        
        if not os.path.exists(input_dir):
            print(f"[SKIP] Input directory not found: {input_dir}")
            continue
        
        print(f"\n[INFO] Processing {site}...")
        run_mock_gan_inference(input_dir, output_dir, model_name='shoreline_gan_mock')
    
    print("\n[SUCCESS] Mock GAN inference complete!")


if __name__ == '__main__':
    main()
