'''February 2016 Aaron Tuor
Tool to make numpy .mat term_doc files from descriptions and dictionary files.
'''
import argparse
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
                    help='Path to folder where dictionary and descriptions are located, and created document '
                                'term matrix will be saved.')
parser.add_argument('dictionary', type=str,
                    help='Name of the file containing line separated words in vocabulary.')
parser.add_argument('descriptions', type=str,
                    help='Name of the file containing line separated text descriptions.')
parser.add_argument('doc_term_file', type=str,
                    help='Name of the file to save the created sparse document term matrix.')
args = parser.parse_args()

# slash ambivalent
if not args.datapath.endswith(slash):
    args.datapath += slash

# make hashmap of words to Integers
dictionaryFile = open(args.datapath + args.dictionary, 'r')
lexicon = dictionaryFile.read().strip().split('\n')
wordmap = {k: v for k, v in zip(lexicon, range(len(lexicon)))}
# open read and write files
outfile = open(args.datapath + args.doc_term_file, "w")
descriptionFile = open(args.datapath + args.descriptions, 'r')
# go through each line in file
docterm = []
for line in descriptionFile:
    countArray = [0] * len(wordmap)  # counts for words in each product description
    lineArray = line.split()
    for word in lineArray:
        if word in wordmap:
            countArray[wordmap[word]] += 1
    docterm.append(countArray)
outfile.close()
doc_term_matrix = sps.csr_matrix(np.array(docterm))
print(doc_term_matrix.shape)
scipy.io.savemat(args.datapath+args.doc_term_file, {'data': doc_term_matrix})