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
parser.add_argument('-item_list', default=[], nargs='+',
                    help='One or more item datafiles to use in the split.')
parser.add_argument('ratings',
                    help='Filename of ratings file datafiles to use in the split.')
parser.add_argument('-user_list', default=[], nargs='+',
                    help='List of user datafiles to use in the split.')
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
item_order = range(num_items)
user_order = range(num_users)
random.shuffle(item_order)
random.shuffle(user_order)

# save shuffled orders
scipy.io.savemat(args.writepath+'item_order.mat', {'data': np.array(item_order)})
scipy.io.savemat(args.writepath+'user_order.mat', {'data': np.array(user_order)})
ratings = ratings[:, item_order]
ratings = ratings[user_order, :]
split_size = num_ratings*0.05

# find item test_cold set
i = num_items
num_cold_test_items = 0
while num_cold_test_items < split_size:
    i = i - 1
    num_cold_test_items = num_cold_test_items + ratings[:, i].getnnz()
item_start_test_cold = i

# find item dev_cold set
num_cold_dev_items = 0
item_end_dev_cold = i
while num_cold_dev_items < split_size:
    i = i - 1
    num_cold_dev_items = num_cold_dev_items + ratings[:, i].getnnz()
item_start_dev_cold = i

#======================================================================
# find user test_cold set
i = num_users
num_cold_test = 0
while num_cold_test < split_size:
    i = i - 1
    num_cold_test = num_cold_test + ratings[i, :].getnnz()
user_start_test_cold = i
# ------------------------------------------------------------

# find user dev_cold set
num_cold_dev = 0
end_dev_cold = i
while num_cold_dev < split_size:
    i = i - 1
    num_cold_dev = num_cold_dev + ratings[i, :].getnnz()
user_start_dev_cold = i
# --------------------------------------------------------------

#========================================================================================
#========================================================================================

#save cold sets
item_test_cold = ratings[0:user_start_dev_cold, item_start_test_cold:num_items]
scipy.io.savemat(args.writepath+'test/features_item_cold.mat', {'data': item_test_cold})
item_dev_cold = ratings[0:user_start_dev_cold, item_start_dev_cold:item_end_dev_cold]
scipy.io.savemat(args.writepath+'dev/features_item_cold.mat', {'data': item_dev_cold})
user_test_cold = ratings[user_start_test_cold:num_users, 0:item_start_dev_cold]
scipy.io.savemat(args.writepath+'test/features_user_cold.mat', {'data': user_test_cold})
user_dev_cold = ratings[user_start_dev_cold:end_dev_cold, 0:item_start_dev_cold]
scipy.io.savemat(args.writepath+'test/features_item_cold.mat', {'data': user_test_cold})
both_cold = ratings[user_start_dev_cold:num_users, item_start_dev_cold: num_items]
scipy.io.savemat(args.writepath+'test/features_both_cold.mat', {'data': both_cold})


# find non cold sets
non_coldratings = ratings[0:user_start_dev_cold, 0:item_start_dev_cold]
[i, j, v] = sps.find(non_coldratings)
num_non_cold = i.shape[0]
numcoldratings = item_test_cold.getnnz() + item_dev_cold.getnnz() + user_test_cold.getnnz() + user_dev_cold.getnnz() + both_cold.getnnz()
split_size = int(round(split_size))
print(split_size)
# find dev set
dev_users = i[range(split_size)]
dev_items = j[range(split_size)]
scipy.io.savemat(args.writepath+'dev/features_user.mat', {'data': i[range(split_size)]})
scipy.io.savemat(args.writepath+'dev/features_item.mat', {'data': j[range(split_size)]})
scipy.io.savemat(args.writepath+'dev/labels_values.mat', {'data': v[range(split_size)]})

# find test set
test_start = split_size
test_end = 2*split_size
test_users = i[test_start:test_end]
test_items = j[test_start:test_end]
scipy.io.savemat(args.writepath+'test/features_user.mat', {'data': i[test_start:test_end]})
scipy.io.savemat(args.writepath+'test/features_item.mat', {'data': j[range(test_start, test_end)]})
scipy.io.savemat(args.writepath+'test/labels_values.mat', {'data': v[range(test_start, test_end)]})

# find train set
train_start = test_end
train_users = i[range(train_start, num_non_cold)]
train_items = j[range(train_start, num_non_cold)]
scipy.io.savemat(args.writepath+'train/features_user.mat', {'data': i[range(train_start, num_non_cold)]})
scipy.io.savemat(args.writepath+'train/features_item.mat', {'data': j[range(train_start, num_non_cold)]})
scipy.io.savemat(args.writepath+'train/labels_values.mat', {'data': v[range(train_start, num_non_cold)]})

numnoncoldratings = v[range(split_size)].shape[0] + v[range(test_start, test_end)].shape[0] + v[range(train_start, num_non_cold)].shape[0]
assert(numcoldratings + numnoncoldratings)

# split extra user and item features
for u in args.user_list:
    namestub = os.path.splitext(os.path.basename(u))[0]
    matrix = loader.import_data(args.readpath + u)
    print(matrix.shape)
    print(dev_users.flatten().shape)
    scipy.io.savemat(args.writepath+'train/features_'+namestub+'.mat',
                     {'data': matrix[user_order[0:user_start_dev_cold]]})
    scipy.io.savemat(args.writepath+'dev/features_'+namestub+'.mat',
                     {'data': matrix[user_order[user_start_dev_cold:user_start_test_cold]]})
    scipy.io.savemat(args.writepath+'test/features_'+namestub+'.mat',
                     {'data': matrix[user_order[user_start_test_cold:num_items]]})
    assert(num_users == matrix.shape[0])
    assert(num_users == (matrix[user_order[0:user_start_dev_cold]].shape[0] +
                         matrix[user_order[user_start_dev_cold:user_start_test_cold]].shape[0] +
                         matrix[user_order[user_start_test_cold:num_items]].shape[0]))

print(args.item_list)
for i in args.item_list:
    namestub = os.path.splitext(os.path.basename(i))[0]
    matrix = loader.import_data(args.readpath + i)
    scipy.io.savemat(args.writepath+'train/features_'+namestub+'.mat',
                     {'data': matrix[item_order[0:item_start_dev_cold]]})
    scipy.io.savemat(args.writepath+'dev/features_'+namestub+'.mat',
                     {'data': matrix[item_order[item_start_dev_cold:item_start_test_cold]]})
    scipy.io.savemat(args.writepath+'test/features_'+namestub+'.mat',
                     {'data': matrix[item_order[item_start_test_cold:num_users]]})
    assert(num_items == matrix.shape[0])
    assert(num_items == (matrix[item_order[0:item_start_dev_cold]].shape[0] +
                         matrix[item_order[item_start_dev_cold:item_start_test_cold]].shape[0] +
                         matrix[item_order[item_start_test_cold:num_users]].shape[0]))



