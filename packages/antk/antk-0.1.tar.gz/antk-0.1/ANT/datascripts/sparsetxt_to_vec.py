'''February 2016 Aaron Tuor
Make vectors of indices and values from sparse matrix format text files
'''
import argparse
import sys
import re
import math
import os
import numpy as np
import scipy.sparse as sps
import scipy.io
slash = '/'
if os.name == 'nt':
    slash = '\\'  # so this works in Windows
# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument('datapath', type=str,
                    help='Path to sparse matrix text file')
parser.add_argument('filename', type=str,
                    help='Name of sparse matrix text file')
args = parser.parse_args()
# slash ambivalent
if not args.datapath.endswith(slash):
    args.datapath += slash

sparse = np.loadtxt(args.datapath + args.filename)
rows = sparse[:, 0]
cols = sparse[:, 1]
vals = sparse[:, 2]

print(rows.shape)
print(cols.shape)
print(vals.shape)
scipy.io.savemat(args.datapath + 'user', {'data': rows})
scipy.io.savemat(args.datapath + 'item', {'data': cols})
scipy.io.savemat(args.datapath + 'values', {'data': vals})
