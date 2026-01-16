"""
Run the full Mombasa shoreline extraction pipeline for a given year.
Usage:
    conda activate shoreline_gan
    python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest
"""

import argparse
import os
from scripts import download_mombasa, preprocess_mombasa, prepare_pix2pix_from_harmonized

def run_year(year, model_name='shoreline_gan_nov', epoch='latest'):
    base_folder = 'data'
    site = f'Mombasa_{year}'
    site_folder = os.path.join(base_folder, site)

    # 1️⃣ Ensure site data exists (download if missing)
    if not os.path.exists(site_folder):
        print(f"[INFO] Site folder {site_folder} not found. Downloading imagery...")
        try:
            download_mombasa.main()
        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            return

    # 2️⃣ Preprocess and harmonize imagery
    print(f"[INFO] Running preprocessing and harmonization for {site}...")
    try:
        preprocess_mombasa.main()
    except AttributeError:
        # fallback in case preprocess_mombasa.main() is missing
        print("[INFO] Using updated main() from robust preprocessing script")
        from scripts.preprocess_mombasa import main as robust_main
        robust_main()
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")
        return

    # 3️⃣ Prepare pix2pix training data
    print(f"[INFO] Preparing pix2pix-ready images for {site}...")
    try:
        prepare_pix2pix_from_harmonized.main(site_folder)
    except Exception as e:
        print(f"[ERROR] Pix2Pix preparation failed: {e}")
        return

    print(f"[SUCCESS] Pipeline completed for {year} using model {model_name}, epoch {epoch}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run shoreline GAN pipeline for Mombasa")
    parser.add_argument('--year', type=int, required=True, help="Year of Mombasa imagery to process")
    parser.add_argument('--model', type=str, default='shoreline_gan_nov', help="Model name")
    parser.add_argument('--epoch', type=str, default='latest', help="Epoch to use")
    args = parser.parse_args()

    run_year(args.year, model_name=args.model, epoch=args.epoch)


import os
from utils.landsat_preproc import harmonize_site

BASE = 'data'
YEARS = [1994, 2004, 2014, 2024]

def main():
    for year in YEARS:
        site = f'Mombasa_{year}'
        site_folder = os.path.join(BASE, site)
        if not os.path.exists(site_folder):
            print(f"Site folder {site_folder} not found. Please run download_mombasa.py first.")
            continue
        print(f"Processing {site_folder}...")
        processed = harmonize_site(site_folder)
        print(f"Wrote {len(processed)} harmonized files for {site}")

if __name__ == "__main__":
    main()

