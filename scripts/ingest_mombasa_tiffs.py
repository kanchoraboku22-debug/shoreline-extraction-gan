"""
Ingest GEE-exported Mombasa RGB TIFFs into the project structure and generate per-year metadata CSVs.

Usage:
    # default: copies files from data/mombasa/ into data/Mombasa_{YEAR}/ and makes metadata CSV
    python scripts/ingest_mombasa_tiffs.py --src data/mombasa

    # move files instead of copying
    python scripts/ingest_mombasa_tiffs.py --src data/mombasa --move

Expect input filenames like: mombasa_1994_RGB.tif
Output per-year folder: data/Mombasa_1994/
Output metadata CSV: data/Mombasa_1994/Mombasa_1994.csv
"""

import os
import re
import shutil
import argparse
from pathlib import Path

try:
    from utils.gdal_modules import gdal_functions_app as gda
except Exception:
    gda = None  # GDAL-based helper may not be installed in lightweight environments


def ingest(src_dir, move=False):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {src_dir}")

    tifs = list(src_dir.glob('*.tif'))
    if not tifs:
        print('No TIFFs found in', src_dir)
        return

    pattern = re.compile(r'mombasa[_-]?(?P<year>\d{4})', flags=re.IGNORECASE)

    for tif in tifs:
        m = pattern.search(tif.stem)
        if not m:
            print('Skipping file (cannot infer year):', tif.name)
            continue
        year = m.group('year')
        site = f'Mombasa_{year}'
        dest_folder = Path('data') / site
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_path = dest_folder / tif.name
        if move:
            shutil.move(str(tif), str(dest_path))
            print(f'Moved {tif.name} -> {dest_path}')
        else:
            shutil.copy2(str(tif), str(dest_path))
            print(f'Copied {tif.name} -> {dest_path}')

        # Create metadata CSV using gdal_get_coords_and_res_list (fallback to rasterio or default metadata)
        csv_path = dest_folder / (site + '.csv')
        try:
            num, csv = gda.gdal_get_coords_and_res_list([str(dest_path)], str(csv_path))
            print(f'Wrote metadata CSV: {csv}')
        except Exception as e:
            # Fallback: try rasterio to read bounds/transform, else write a minimal CSV assuming EPSG:32737 and 30m resolution
            try:
                import rasterio
                with rasterio.open(str(dest_path)) as src:
                    bounds = src.bounds
                    transform = src.transform
                    cols = src.width
                    rows = src.height
                    xres = abs(transform.a)
                    yres = abs(transform.e)
                    epsg = int(src.crs.to_epsg()) if src.crs else 32737
                import csv
                with open(str(csv_path), 'w', newline='') as cf:
                    writer = csv.writer(cf)
                    writer.writerow(['file','xmin','ymin','xmax','ymax','xres','yres','epsg','cols','rows'])
                    writer.writerow([str(dest_path), bounds.left, bounds.bottom, bounds.right, bounds.top, xres, yres, epsg, cols, rows])
                print(f'Wrote fallback metadata CSV: {csv_path}')
            except Exception:
                import csv
                with open(str(csv_path), 'w', newline='') as cf:
                    writer = csv.writer(cf)
                    writer.writerow(['file','xmin','ymin','xmax','ymax','xres','yres','epsg','cols','rows'])
                    writer.writerow([str(dest_path),'','','','',30,30,32737,'',''])
                print(f'Wrote minimal metadata CSV (default EPSG:32737): {csv_path}')

    print('\nIngest finished. You can now run:')
    print('  python scripts/preprocess_mombasa.py')
    print('  python scripts/prepare_pix2pix_from_harmonized.py')
    print('  python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, default='data/mombasa', help='Source folder containing GEE-exported TIFFs')
    parser.add_argument('--move', action='store_true', help='Move files instead of copying')
    args = parser.parse_args()
    ingest(args.src, move=args.move)
