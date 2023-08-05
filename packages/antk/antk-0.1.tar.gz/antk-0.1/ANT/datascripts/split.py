'''February 2016 Aaron Tuor
Tool to make 5/5/5/5/80, coldDev, coldTest, dev, test, train datasplit for movielens 100k with imdb plot descriptions.
'''
import argparse
import os
import scipy.sparse as sps
import scipy.io
import loader
import random
import numpy as np

slash = '/'
if os.name == 'nt':
    slash = '\\'  # so this works in Windows

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument('readpath', type=str,
                    help='Path to folder where data to be split is located.')
parser.add_argument('writepath', type=str,
                    help='Path to folder where split data is to be stored: Folder must contain, train, dev and'
                         'test directories.')
parser.add_argument('ratings',
                    help='Filename of ratings file datafiles to use in the split.')
args = parser.parse_args()

# slash ambivalent
if not args.readpath.endswith(slash):
    args.readpath += slash
if not args.writepath.endswith(slash):
    args.writepath += slash

loader.makedirs(args.writepath)

# read utility matrix and independently shuffle rows and columns
ratings = loader.import_data(args.readpath + args.ratings)
num_users = ratings.shape[0]
num_items = ratings.shape[1]
num_ratings = ratings.getnnz()
order = range(num_ratings)
print(len(order))
random.shuffle(order)
split_size = int(round(num_ratings*.1))

# save shuffled orders
scipy.io.savemat(args.writepath+'order.mat', {'data': np.array(order)})



#========================================================================================
#========================================================================================
def toOnehot(X, dim):
    #empty one-hot matrix
    hotmatrix = np.zeros((X.shape[0], dim))
    #fill indice positions
    hotmatrix[np.arange(X.shape[0]), X] = 1
    hotmatrix = sps.csr_matrix(hotmatrix)
    return hotmatrix

# split
[i, j, v] = sps.find(ratings)
i = i[order]
j = j[order]
v = v[order]
# find dev set
print(split_size)
dev_users = i[range(split_size)]
dev_items = j[range(split_size)]
scipy.io.savemat(args.writepath+'dev/features_user.mat', {'data': toOnehot(dev_users, num_users)})
scipy.io.savemat(args.writepath+'dev/features_item.mat', {'data': toOnehot(dev_items, num_items)})
scipy.io.savemat(args.writepath+'dev/labels_values.mat', {'data': v[range(split_size)]})

# find test set
test_start = split_size
test_end = 2*split_size
test_users = i[test_start:test_end]
test_items = j[test_start:test_end]
scipy.io.savemat(args.writepath+'test/features_user.mat', {'data': toOnehot(test_users, num_users)})
scipy.io.savemat(args.writepath+'test/features_item.mat', {'data': toOnehot(test_items, num_items)})
scipy.io.savemat(args.writepath+'test/labels_values.mat', {'data': v[test_start:test_end]})

# find train set
train_start = test_end
train_users = i[range(train_start, num_ratings)]
train_items = j[range(train_start, num_ratings)]
scipy.io.savemat(args.writepath+'train/features_user.mat', {'data': toOnehot(train_users, num_users)})
scipy.io.savemat(args.writepath+'train/features_item.mat', {'data': toOnehot(train_items, num_items)})
scipy.io.savemat(args.writepath+'train/labels_values.mat', {'data': v[train_start:num_ratings]})

numnoncoldratings = v[range(split_size)].shape[0] + v[range(test_start, test_end)].shape[0] + v[range(train_start, num_ratings)].shape[0]

assert(numnoncoldratings == num_ratings)

