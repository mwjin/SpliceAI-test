#!/extdata6/Doyeon/anaconda3/envs/minu-py2/bin/python2
"""
Statistics for the result of 'test_model.py'
"""

import os
import pickle
import sys
from utils import *

from constants import RESULT_DIR

test_result_path = sys.argv[1]
result_basename = os.path.basename(test_result_path)
result_prefix = os.path.splitext(result_basename)[0]

with open(test_result_path, 'rb') as infile:
    test_result = pickle.load(infile)


output_class_labels = ['Acceptor', 'Donor']

for output_class in [0, 1]:
    print "\n\033[1m%s:\033[0m" % (output_class_labels[output_class])

    pr_curve_title = result_prefix + '_%s' % output_class_labels[output_class]
    pr_curve_path = '%s/%s_%s.png' % (RESULT_DIR, result_prefix, output_class_labels[output_class])

    Y_true, Y_pred = np.asarray(test_result[output_class])

    for t in range(1):
        print_topl_statistics(Y_true[t], Y_pred[t])
        auc = draw_pr_curve(Y_true[t], Y_pred[t], title=pr_curve_title, plot_path=pr_curve_path)
        print('AUC\t%.4f' % auc)
