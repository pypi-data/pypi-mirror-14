'''Jan 2016 Aaron Tuor
Tool to process Movielens 100k Metadata
'''
import argparse
import numpy
import scipy.sparse as sps
import os
import scipy.io

slash = '/'
if os.name == 'nt':
    slash = '\\'  # so this works in Windows
parser = argparse.ArgumentParser()
parser.add_argument('datapath', type=str)
parser.add_argument('outpath', type=str, default='')
args = parser.parse_args()
if not args.datapath.endswith(slash):
    args.datapath += slash
infile = open(args.datapath + 'u.occupation', 'r')
occlist = infile.read()
occlist = occlist.split('\n')
occmap = {k: v for k, v in zip(occlist, range(len(occlist)))}
monthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthmap = {k: v for k, v in zip(monthlist, range(1, 13))}
print(monthmap)
infile.close()
user_features = []
with open(args.datapath + 'u.user') as infile:
    first = False
    lines = infile.readlines()
    for line in lines:
        user_feature_list = []
        line = line.split('|')
        # age==================================
        age = float(line[1]) / 100
        user_feature_list.append(age)
        # sex==================================
        if line[2] == 'M':
            user_feature_list.append(1.0)
            user_feature_list.append(0.0)
        else:
            user_feature_list.append(0.0)
            user_feature_list.append(1.0)
        # occupation==================================
        occupation = [0.0] * len(occlist)
        occupation[occmap[line[3]]] = 1.0
        user_feature_list.extend(occupation)
        # first zip code digit: large geographical areas
        zip1 = [0.0] * 10
        if not line[4].isdigit():
            line[4] = '00000'
        zip1[int(line[4][0])] = 1.0
        user_feature_list.extend(zip1)
        # next two digits: regional centers
        zip2 = [0.0] * 100
        zip2[int(line[4][1:3])] = 1.0
        user_feature_list.extend(zip2)
        user_features.append(user_feature_list)
        user_feature_matrix = numpy.array(user_features)
        user_feature_matrix = sps.csr_matrix(user_feature_matrix)
        print(user_feature_matrix.shape)
    scipy.io.savemat(args.outpath, {'data': user_feature_matrix})
