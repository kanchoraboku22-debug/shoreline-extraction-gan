import numpy as np
from utils.validation import binary_metrics


def test_iou_precision_recall():
    gt = np.array([[1,1,0],[0,1,0],[0,0,0]], dtype=np.uint8)
    pred = np.array([[1,0,0],[0,1,0],[0,0,0]], dtype=np.uint8)
    m = binary_metrics(pred, gt, threshold=0.5)
    # tp = 2 (positions (0,0) and (1,1)), fp = 0, fn = 1 (0,1)
    assert m['tp'] == 2
    assert m['fp'] == 0
    assert m['fn'] == 1
    assert abs(m['iou'] - (2/(2+0+1))) < 1e-6
    assert abs(m['precision'] - 1.0) < 1e-6
    assert abs(m['recall'] - (2/(2+1))) < 1e-6
