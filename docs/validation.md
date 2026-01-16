# Validation and Accuracy Assessment ✅

This document explains how to run basic validation for predicted shoreline segmentation masks against available ground truth data.

Metrics implemented:
- IoU (Intersection over Union)
- Precision
- Recall

Script:
- `scripts/validate_against_gt.py` — expects a `model_outputs/gan` (or other) folder containing predicted masks and a `ground_truth/` folder with matching GT masks.

Usage:

    conda activate shoreline_gan
    python scripts/validate_against_gt.py

Output:
- `results/validation_metrics.csv` with per-image IoU, precision, recall, TP/FP/FN counts.

Notes:
- The script expects file name correspondence between predictions and GT. For complex mapping, you can modify the script to read a CSV mapping.
- For vector GT (shorelines in shapefiles), consider rasterizing the vector shorelines to the same grid before metric computation (future work / extension).
