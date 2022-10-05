#!/usr/bin/python3

# script for processing .012 output from VCF into a format which can be read by the MST linakge mapping software

from os import listdir
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Organizes data from VCF into a format which can be read by MSTLinkage.')
parser.add_argument('--header', help='header file with options for how the program is run', default='v2mHeader.txt')
parser.add_argument('--output', help='filename for the output file', default='readyForMCT')
parser.add_argument('--deleteIndex', help='deletes the first column of the file (y/n)', default="y")
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

indx012 = 1
indxIndv = 2
indxPos = 3
headerContent = []

# extract filenames from header
with open(args.header) as headerFile:
    for line in headerFile:
        headerContent.append(line.strip()) 
        
#TODO: can make this more robust by finding "# INPUT FILES" and then grabbing filenames from that index
file012 = pd.read_csv(headerContent[indx012], sep='\t', header = None)
fileIndv = pd.read_csv(headerContent[indxIndv], sep='\t', header = None)
filePos = pd.read_csv(headerContent[indxPos], sep='\n', header = None)
headerFile.close()

# delete the index of the 012 file and transpose
file012 = file012.drop(file012.columns[0], axis = 1)
file012T = file012.transpose()
file012T.reset_index(drop=True, inplace=True)

# replace tab with underscore in filePos 
filePosUnder = filePos.replace(to_replace='\t', regex=True, value='_')

# make filePosUnder first column in file012T
file012T.insert(0, column=None, value=filePosUnder)
temp = file012T.transpose()
temp.reset_index(drop=True, inplace=True)
file012T = temp.transpose()

# convert numbers to alpha and create a copy of the inverse conversion
alphaFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'A', 'B', 'A'])
alphaInverseFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'B', 'A', 'B'])

#TODO: create the same thing but for husband's method

# combine alphaFile and alphaFileInverse
combo = pd.concat([alphaFile, alphaInverseFile])
combo.reset_index(drop=True, inplace=True)

#TODO: strip (.all.bam) extension

# insert top row using transposed fileIndv
fileIndvIns = pd.DataFrame([['locus']], columns=fileIndv.columns)
fileIndv2 = pd.concat([fileIndvIns, fileIndv])
fileIndv2.reset_index(drop=True, inplace=True)
fileIndvT = fileIndv2.transpose()
headerless = pd.concat([fileIndvT, combo])
headerless.reset_index(drop=True, inplace=True)

# extract MCTHeader TODO: make if statements finding loci and pop_num and adding them automatically
index = 0
MCTHeader = []
for line2 in headerContent:
    index += 1
    if line2 == '# MCT HEADER':
        while True:
            if index >= len(headerContent):
                break
            #tempList = headerContent[index].split()    might be usefull for forcing tab separation in MCTHeader 
            MCTHeader.append(headerContent[index] + '\n')
            index += 1
MCTHeader.append('\n')

# write header and dataframe to file
with open(args.output, 'x') as toWrite:
    toWrite.writelines(MCTHeader)
toWrite.close()
headerless.to_csv(args.output, mode='a', sep='\t', header=None, index=None)     