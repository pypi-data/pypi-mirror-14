'''
normalize.py  : Text normalization script
authors       : Elliot Starks, Aaron Tuor, Samuel Nguyen
last modified : August, 2015
'''

#!/user/bin/env python

import argparse
import sys
import re

# Handle arguments
arguments = sys.argv
if len(arguments) < 1:
    print 'Usage: <infile>'
    sys.exit();

infile = open(arguments[1], 'r')
namestub = arguments[1].split('.')[0].strip()
extension = arguments[1].split('.')[1].strip()
newfile = namestub + '_norm.' + extension
outfile = open(newfile, 'w')

# Pre-compile regular expressions
regexPunc = re.compile(r"[^A-Za-z0-9']")

# Process each line
for line in infile:
    line = regexPunc.sub(" ", line)#replace punctuation with space excepting apostrophes
    line = line.lower() # make everything lowercase		
    wordlist = line.split(" ")#make an array of words to individually work on words
	
# Process each word; write words delimited by space to file
    for word in wordlist:
	word = word.strip('\'') #yank out leading and trailing quotation marks
	word = word.strip()
	if word != '':
		outfile.write(word)
		outfile.write(' ')
    outfile.write("\n")
outfile.close()




