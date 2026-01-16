"""
Lightweight Landsat preprocessing and harmonization utilities.
- Uses existing CoastSat preprocess functions where possible
- Produces harmonized GeoTIFFs with consistent bands: B,G,R,NIR,SWIR1
- Tries to use rasterio to write outputs, falls back to GDAL-based writer
"""
import os
import glob
import numpy as np
from pathlib import Path

try:
    import rasterio
    from rasterio.transform import Affine
    _HAS_RASTERIO = True
except Exception:
    _HAS_RASTERIO = False

from utils.coastsat import SDS_preprocess2
from utils.gdal_modules import gdal_functions_app as gda


def write_geotiff(path, arr, georef, projection_wkt):
    """Write a multi-band GeoTIFF using rasterio if available, else GDAL."""
    # arr shape: (rows, cols, bands)
    rows, cols, bands = arr.shape
    if _HAS_RASTERIO:
        transform = Affine(georef[1], georef[2], georef[0], georef[3], georef[4], georef[5])
        crs = projection_wkt
        with rasterio.open(
            path,
            'w',
            driver='GTiff',
            height=rows,
            width=cols,
            count=bands,
            dtype=arr.dtype,
            transform=transform,
            crs=crs,
        ) as dst:
            for i in range(bands):
                dst.write(arr[:,:,i], i+1)
    else:
        # Fall back to GDAL
        driver = gda.gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(path, cols, rows, bands, gda.gdal.GDT_Float32)
        out_ds.SetGeoTransform(tuple(georef))
        out_ds.SetProjection(projection_wkt)
        for i in range(bands):
            out_ds.GetRasterBand(i+1).WriteArray(arr[:,:,i])
        out_ds.FlushCache()
        out_ds = None


def harmonize_site(site_folder, out_folder=None, target_bands=5):
    """Process images in a site folder and save harmonized GeoTIFFs.
    - Looks for geotiffs in L5, L7, L8 subfolders
    - Uses SDS_preprocess2.preprocess_single to get band arrays
    - Performs per-band histogram matching to the first valid image (reference)
    """
    if out_folder is None:
        out_folder = os.path.join(site_folder, 'harmonized')
    Path(out_folder).mkdir(parents=True, exist_ok=True)

    # search for tif files recursively
    tifs = glob.glob(os.path.join(site_folder, '**', '*.tif'), recursive=True)
    processed = []
    ref = None

    for tif in tifs:
        try:
            # Heuristic: find sensor from filename
            basename = os.path.basename(tif)
            if '_L8_' in basename or '_L8' in basename:
                sat = 'L8'
            elif '_L7_' in basename or '_L7' in basename:
                sat = 'L7'
            elif '_L5_' in basename or '_L5' in basename:
                sat = 'L5'
            else:
                # Try to infer from folder names
                if '/L8/' in tif.replace('\\','/'):
                    sat = 'L8'
                elif '/L7/' in tif.replace('\\','/'):
                    sat = 'L7'
                elif '/L5/' in tif.replace('\\','/'):
                    sat = 'L5'
                else:
                    sat = None

            # Construct input for preprocess_single depending on satellite
            if sat in ['L7', 'L8']:
                # Expect pan and ms naming convention from SDS_download
                # e.g., ..._pan.tif and ..._ms.tif
                if tif.endswith('_pan.tif'):
                    # find corresponding ms file by name
                    ms_candidate = tif.replace('_pan.tif', '_ms.tif')
                    if not os.path.exists(ms_candidate):
                        # try alternate pattern
                        ms_candidate = tif.replace('_pan.tif', '.tif')
                    fn = [tif, ms_candidate]
                elif tif.endswith('_ms.tif'):
                    pan_candidate = tif.replace('_ms.tif', '_pan.tif')
                    fn = [pan_candidate, tif]
                else:
                    # fallback: try using tif as ms only
                    fn = [tif]
            else:
                fn = tif

            # preprocess_single returns im_ms (rows, cols, bands), georef, cloud_mask, im_extra, im_QA, im_nodata
            im_ms, georef, cloud_mask, im_extra, im_QA, im_nodata = SDS_preprocess2.preprocess_single(fn, sat if sat else 'L8', False)

            # select first 5 bands (B,G,R,NIR,SWIR) if available
            if im_ms.ndim == 3 and im_ms.shape[2] >= 5:
                arr = im_ms[:,:,:5]
            else:
                # pad or skip
                continue

            # set reference
            if ref is None:
                ref = arr.copy()
                ref_georef = georef
                # determine projection from file using GDAL
                ds = gda.gdal.Open(tif)
                proj = ds.GetProjection()
                ds = None
                ref_proj = proj

                # write ref directly
                outname = os.path.join(out_folder, os.path.basename(tif).replace('.tif', '_harm.tif'))
                write_geotiff(outname, arr.astype('float32'), georef, ref_proj)
                processed.append(outname)
                continue

            # histogram match each band to the reference
            matched = np.zeros_like(arr, dtype='float32')
            for b in range(arr.shape[2]):
                try:
                    matched[:,:,b] = SDS_preprocess2.hist_match(arr[:,:,b], ref[:,:,b])
                except Exception:
                    matched[:,:,b] = arr[:,:,b]

            outname = os.path.join(out_folder, os.path.basename(tif).replace('.tif', '_harm.tif'))
            write_geotiff(outname, matched.astype('float32'), georef, ref_proj)
            processed.append(outname)

        except Exception as e:
            print(f"Skipping {tif}: preprocess failed with {e}")
            continue

    print(f"Harmonization complete. {len(processed)} files written to {out_folder}")
    return processed
