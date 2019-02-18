#!/extdata6/Doyeon/anaconda3/envs/minu-py2/bin/python2
###############################################################################
# This file contains code to test the SpliceAI model.
###############################################################################

import sys
import time
import h5py
import pickle
from keras.models import load_model
from utils import *
from constants import *

assert int(sys.argv[1]) in [80, 400, 2000, 10000]
CL = int(sys.argv[1])

###############################################################################
# Load model and test data
###############################################################################

BATCH_SIZE = 6
version = [1, 2, 3, 4, 5]

model = [[] for v in range(len(version))]

for v in range(len(version)):
    model[v] = load_model('%s/spliceai%s.h5' % (MODEL_DIR, str(version[v])))

dataset_path = sys.argv[2]
h5f = h5py.File(dataset_path, 'r')

result_path = sys.argv[3]

num_idx = len(h5f.keys())//2

###############################################################################
# Model testing
###############################################################################

start_time = time.time()

output_class_labels = ['Null', 'Acceptor', 'Donor']
# The three neurons per output correspond to no splicing, splice acceptor (AG)
# and splice donor (GT) respectively.

Y_true_acceptor = [[] for t in range(1)]
Y_pred_acceptor = [[] for t in range(1)]
Y_true_donor = [[] for t in range(1)]
Y_pred_donor = [[] for t in range(1)]

for idx in range(num_idx):

    X = h5f['X' + str(idx)][:]
    Y = h5f['Y' + str(idx)][:]

    Xc, Yc = clip_datapoints(X, Y, CL, 1)

    Yps = [np.zeros(Yc[0].shape) for t in range(1)]

    for v in range(len(version)):

        Yp = model[v].predict(Xc, batch_size=BATCH_SIZE)

        if not isinstance(Yp, list):
            Yp = [Yp]

        for t in range(1):
            Yps[t] += Yp[t]/len(version)
    # Ensemble averaging (mean of the ensemble predictions is used)

    for t in range(1):

        is_expr = (Yc[t].sum(axis=(1,2)) >= 1)

        # acceptor
        Y_true_acceptor[t].extend(Yc[t][is_expr, :, 1].flatten())
        Y_pred_acceptor[t].extend(Yps[t][is_expr, :, 1].flatten())
        Y_true_donor[t].extend(Yc[t][is_expr, :, 2].flatten())
        Y_pred_donor[t].extend(Yps[t][is_expr, :, 2].flatten())

h5f.close()

test_result = [[Y_true_acceptor, Y_pred_acceptor], [Y_true_donor, Y_pred_donor]]

with open(result_path, 'wb') as outfile:
    pickle.dump(test_result, outfile)

print "--- %s seconds ---" % (time.time() - start_time)
print "--------------------------------------------------------------"


###############################################################################

