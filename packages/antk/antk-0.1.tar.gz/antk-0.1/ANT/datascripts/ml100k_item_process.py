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
monthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthmap = {k: v for k, v in zip(monthlist, range(12))}
infile.close()
item_features = []
with open(args.datapath + 'u2.item') as infile:
    first = False
    lines = infile.readlines()
    for line in lines:
        item_feature_list = []
        line = line.split('|')
        # month released==================================
        date = line[2].split('-')
        months = [0.0]*12
        months[monthmap[date[1]]] = 1.0
        item_feature_list.extend(months)
        # year released==================================
        item_feature_list.append(float(int(date[2]) - 1930)/(2016.0-1930.0))
        print(line)
        genres = line[5:len(line)]
        for i in range(len(genres)):
            genres[i] = float(genres[i])
        item_feature_list.extend(genres)
        item_features.append(item_feature_list)
        print(len(item_features))
    item_feature_matrix = numpy.array(item_features)
    item_feature_matrix = sps.csr_matrix(item_feature_matrix)
    print(item_feature_matrix.shape)
    scipy.io.savemat(args.outpath, {'data': item_feature_matrix})