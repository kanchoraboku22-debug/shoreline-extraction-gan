# Usage: Mombasa Study Area (1994, 2004, 2014, 2024)

This document explains how to download and preprocess Landsat imagery for the Mombasa coastline using the repo's utilities.

1. Ensure your environment is ready (see `docs/environment_setup.md`) and the `shoreline_gan` env is active.

2. Download imagery for each epoch (runs CoastSat-based downloader):

    python scripts/download_mombasa.py

   This creates `data/Mombasa_1994`, `data/Mombasa_2004`, etc.

3. Preprocessing (to be run next): atmospheric correction, cloud masking and harmonization.

   Run the harmonization script (created in this branch) which uses CoastSat preprocessing and saves harmonized GeoTIFFs suitable for the GAN model:

       conda activate shoreline_gan
       python scripts/preprocess_mombasa.py

   The script will write harmonized TIFFs to `data/Mombasa_{YEAR}/harmonized/` for each year.

   Note: `utils/landsat_preproc.py` performs per-band histogram matching and resampling. This is a pragmatic harmonization step; for publication-quality harmonization consider full surface reflectance normalization and BRDF corrections (future work).
Notes:
- The downloader uses CoastSat/GEE backend and respects cloud threshold settings in `utils/download_utils.py`.
- For 2024 the script prefers Landsat 9 where available; if not, Landsat 8 will be used.
- The output metadata CSVs will be saved into each `data/Mombasa_*` folder.

### If you exported TIFFs from GEE directly

If you export TIFFs from GEE (recommended workflow for small samples), place them in a folder (example: `data/mombasa/`) and run the helper script to ingest them into the project layout and generate metadata CSVs:

    conda activate shoreline_gan
    python scripts/ingest_mombasa_tiffs.py --src data/mombasa

Optional: add `--move` to move files instead of copying.

Expected results after running the helper:

```
data/Mombasa_1994/mombasa_1994_RGB.tif
data/Mombasa_1994/Mombasa_1994.csv
data/Mombasa_2004/mombasa_2004_RGB.tif
data/Mombasa_2004/Mombasa_2004.csv
...
```

These per-year folders and CSVs let you run the downstream steps (`preprocess_mombasa.py`, `prepare_pix2pix_from_harmonized.py`, and `run_pipeline_mombasa.py`) without using the CoastSat downloader.

### Prepare input for GAN (pix2pix)

After harmonization, convert harmonized GeoTIFFs to RGB JPEGs and create pix2pix-ready 256x256 splits:

    python scripts/prepare_pix2pix_from_harmonized.py

This writes JPEGs to `data/Mombasa_{YEAR}/jpg_files/preprocessed` and pix2pix-ready images to `data/Mombasa_{YEAR}/jpg_files/pix2pix_ready` which are compatible with the existing GUI and training routines.

### Run inference

You can run inference via the GUI (`python shoreline_gan_gui.py`) or via the provided end-to-end pipeline script.

End-to-end pipeline for a single year (download, harmonize, prepare pix2pix, run GAN, extract shorelines):

    conda activate shoreline_gan
    python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest

This will write outputs to `model_outputs/gan/Mombasa_2014/...` and processed shorelines in `model_outputs/processed/Mombasa_2014/`.

If you prefer the GUI mode, you can point the GUI to the `data/Mombasa_2014/jpg_files/pix2pix_ready` folder (or use the `shoreline_gan_gui.py` Preprocess and Shoreline Extraction buttons).