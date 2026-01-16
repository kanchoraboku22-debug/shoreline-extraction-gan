# Model adaptation notes 🔧

Goal: Accept multi-sensor harmonized inputs (L5/L7/L8/L9) while keeping the core GAN architecture unchanged.

Summary of approach:
- Harmonization: produce standardized GeoTIFFs with consistent band order (B, G, R, NIR, SWIR1) and resolution.
- Input to GAN: generate RGB composites (B,G,R) from the harmonized TIFFs and feed them as 3-channel inputs to the existing pix2pix model.
  - Rationale: minimizes changes to the core generator and discriminator; uses already validated pix2pix U-Net architecture.
- Optional extension: include NIR as an extra channel by retraining/fine-tuning the generator to accept 4 or 5 channels. This requires changing `--input_nc` and retraining the model; avoid unless necessary.

Fine-tuning workflow (optional):
- Prepare paired training data (A: RGB/harmonized composite, B: binary shoreline masks) as per existing pix2pix data conventions.
- Train using `pix2pix_modules/train.py`, set `--input_nc 3` (or 4/5 if adding NIR) and relevant options in `options/train_options.py`.

Assumptions and limitations:
- Histogram matching across images is a pragmatic harmonization step but is not a full radiometric harmonization (no BRDF correction or full surface reflectance normalization). For publication-quality harmonization further correction is recommended (discuss in limitations chapter).
- The current pipeline uses RGB composites; sensor differences are expected to be mitigated but not fully eliminated.

Files of interest:
- `utils/landsat_preproc.py` – harmonization implementation (histogram matching, TIFF writer)
- `scripts/prepare_pix2pix_from_harmonized.py` – converts harmonized TIFFs to RGB JPEGs and produces pix2pix-ready splits
- `docs/usage_mombasa.md` – instructions to run the pipeline

Next steps:
- Validate harmonization across sensors using sample images and consider band-normalization using invariant targets (e.g., pseudo-invariant features) if necessary.
