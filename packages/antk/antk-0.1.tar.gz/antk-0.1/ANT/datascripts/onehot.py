import loader
import scipy.io as sio

a = loader.read_data_sets('/home/aarontuor/data/ml100k')
a.show()
devhots = loader.toOnehot(a.dev.labels['ratings'] -1, 5)
# trainhots = loader.toOnehot(a.train.labels['ratings'] -1, 5)
testhots = loader.toOnehot(a.test.labels['ratings'] -1, 5)
print(devhots.todense().shape)

loader.smatsave('/home/aarontuor/test.sparse', devhots.todense())