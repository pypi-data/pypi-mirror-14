import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('folderpath', type=str)
args = parser.parse_args()
folder = args.folderpath
if folder.endswith('/'):
    folder = folder[0:len(folder)-1]
os.system('mkdir ' + folder)
os.system('mkdir ' + folder + '/dev')
os.system('mkdir ' + folder + '/train')
os.system('mkdir ' + folder + '/test')

