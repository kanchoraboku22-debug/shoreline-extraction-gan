"""
Validation utilities: IoU, precision, recall for binary masks.
"""
import numpy as np


def binary_metrics(pred, gt, threshold=0.5):
    """Compute IoU, precision, recall for binary arrays.
    pred, gt: numpy arrays (float or bool), same shape
    threshold: threshold to binarize pred if float
    """
    if pred.dtype != bool:
        pred_bin = pred >= threshold
    else:
        pred_bin = pred
    gt_bin = gt.astype(bool)

    tp = np.logical_and(pred_bin, gt_bin).sum()
    fp = np.logical_and(pred_bin, np.logical_not(gt_bin)).sum()
    fn = np.logical_and(np.logical_not(pred_bin), gt_bin).sum()

    iou = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        'iou': float(iou),
        'precision': float(precision),
        'recall': float(recall),
        'tp': int(tp),
        'fp': int(fp),
        'fn': int(fn)
    }
