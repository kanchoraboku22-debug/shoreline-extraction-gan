"""
Validate predicted binary masks against ground truth masks and produce a CSV summary.
Assumes filenames correspond (e.g., image_01_pred.tif vs image_01_gt.tif) or provides a mapping CSV.
"""
import os
import glob
import numpy as np
import rasterio
import pandas as pd
from utils.validation import binary_metrics

PRED_FOLDER = 'model_outputs/gan'
GT_FOLDER = 'ground_truth'
OUT_CSV = 'results/validation_metrics.csv'

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

preds = glob.glob(os.path.join(PRED_FOLDER, '*_pred*.tif')) + glob.glob(os.path.join(PRED_FOLDER, '*_pred*.png'))
if len(preds) == 0:
    print('No predicted masks found in', PRED_FOLDER)
else:
    rows = []
    for pred in preds:
        name = os.path.splitext(os.path.basename(pred))[0]
        # try to find matching gt
        gt_candidate = os.path.join(GT_FOLDER, name.replace('_pred','') + '.tif')
        if not os.path.exists(gt_candidate):
            gt_candidate = os.path.join(GT_FOLDER, name.replace('_pred','') + '.png')
        if not os.path.exists(gt_candidate):
            print('No GT found for', pred, '-> skipping')
            continue
        with rasterio.open(pred) as src:
            pred_arr = src.read(1)
        with rasterio.open(gt_candidate) as src:
            gt_arr = src.read(1)
        # threshold if continuous
        metrics = binary_metrics(pred_arr, gt_arr, threshold=0.5)
        metrics['file'] = name
        rows.append(metrics)

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print('Saved validation metrics to', OUT_CSV)
