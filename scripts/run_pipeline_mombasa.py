"""
End-to-end pipeline for Mombasa (single-year runs).
Usage example:
    conda activate shoreline_gan
    python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest
"""
import argparse
import os
from scripts import download_mombasa, preprocess_mombasa, prepare_pix2pix_from_harmonized
from utils import gan_inference_utils


def run_year(year, model_name='shoreline_gan_nov', epoch='latest'):
    site = f'Mombasa_{year}'
    base = 'data'
    site_folder = os.path.join(base, site)

    # Download (if necessary)
    if not os.path.exists(site_folder):
        print('Downloading imagery...')
        download_mombasa.main()
    else:
        print('Site folder exists; skipping download.')

    # Preprocess/harmonize
    print('Running harmonization...')
    preprocess_mombasa.main()

    # Prepare pix2pix inputs
    print('Preparing pix2pix inputs...')
    os.system('python scripts/prepare_pix2pix_from_harmonized.py')

    # Run GAN and postprocess
    source = os.path.join(site_folder, 'jpg_files', 'pix2pix_ready')
    coords_csv = os.path.join(site_folder, site + '.csv')
    outputs_dir = os.path.join(os.getcwd(), 'model_outputs')
    if not os.path.exists(source):
        raise FileNotFoundError(f'Pix2pix source folder not found: {source}')

    print('Running GAN inference and extracting shorelines...')
    gan_inference_utils.run_and_process(site, source, model_name, coords_csv, epoch=epoch)
    print('Pipeline finished for year', year)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True, help='Year to run (1994/2004/2014/2024)')
    parser.add_argument('--model', default='shoreline_gan_nov', help='Model name in checkpoints')
    parser.add_argument('--epoch', default='latest', help='Epoch to load')
    args = parser.parse_args()
    run_year(args.year, model_name=args.model, epoch=args.epoch)
