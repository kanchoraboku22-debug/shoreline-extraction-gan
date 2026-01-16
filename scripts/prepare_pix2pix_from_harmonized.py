"""
Convert harmonized GeoTIFFs (B,G,R,NIR,SWIR) into RGB JPEGs and create pix2pix-ready splits (256x256).
"""
import os
import glob
import numpy as np
import cv2
from utils import image_processing_utils

BASE = 'data'
YEARS = [1994, 2004, 2014, 2024]

for year in YEARS:
    site = f'Mombasa_{year}'
    harmonized_folder = os.path.join(BASE, site, 'harmonized')
    if not os.path.exists(harmonized_folder):
        print(f"No harmonized folder for {site}, skipping. Run scripts/preprocess_mombasa.py first.")
        continue
    out_preprocessed = os.path.join(BASE, site, 'jpg_files', 'preprocessed')
    os.makedirs(out_preprocessed, exist_ok=True)
    tifs = glob.glob(os.path.join(harmonized_folder, '*_harm.tif'))
    count = 0
    for tif in tifs:
        try:
            # read using OpenCV via gdal path if available or use rasterio
            import rasterio
            with rasterio.open(tif) as src:
                arr = src.read()  # (bands, rows, cols)
                arr = np.transpose(arr, [1,2,0])
        except Exception:
            # fallback to gdal
            from osgeo import gdal
            ds = gdal.Open(tif)
            bands = [ds.GetRasterBand(i+1).ReadAsArray() for i in range(ds.RasterCount)]
            arr = np.transpose(np.array(bands), [1,2,0])
            ds = None

        # Expect at least 3 bands B,G,R in first three positions
        if arr.shape[2] < 3:
            continue
        rgb = arr[:,:,:3]
        # Normalize to 0-255 for JPEG
        def scale_to_uint8(x):
            x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
            p2 = np.nanpercentile(x, 2)
            p98 = np.nanpercentile(x, 98)
            if p98 - p2 <= 0:
                scaled = np.zeros_like(x, dtype='uint8')
            else:
                scaled = 255.0 * (x - p2) / (p98 - p2)
                scaled = np.clip(scaled, 0, 255).astype('uint8')
            return scaled

        rgb_u8 = np.zeros_like(rgb, dtype='uint8')
        for b in range(3):
            rgb_u8[:,:,b] = scale_to_uint8(rgb[:,:,b])

        out_name = os.path.join(out_preprocessed, os.path.splitext(os.path.basename(tif))[0] + '.jpg')
        cv2.imwrite(out_name, rgb_u8[:,:,[2,1,0]])  # convert to BGR for OpenCV
        count += 1

    print(f"Wrote {count} JPEGs to {out_preprocessed} for {site}")

    # Create pix2pix_ready splits
    pix2pix_ready = os.path.join(BASE, site, 'jpg_files', 'pix2pix_ready')
    os.makedirs(pix2pix_ready, exist_ok=True)
    image_processing_utils.split_and_resize(out_preprocessed, pix2pix_ready, ext='.jpg')
    print(f"Created pix2pix-ready images in {pix2pix_ready}")
