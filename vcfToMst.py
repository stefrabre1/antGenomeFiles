#!/usr/bin/python3

# script for processing .012 output from VCF into a format which can be read by the MST linakge mapping software

from os import listdir
import argparse
import pandas as pd

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Organizes data from VCF into a format which can be read by MSTLinkage.')
parser.add_argument('--header', help='header file with options for how the program is run', default='v2mHeader.txt')
parser.add_argument('--output', help='filename for the output file', default='readyForMST.txt')
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# Define constants
indx012 = 1
indxIndv = 2
indxPos = 3
headerContent = []

# Finds the index of where specific data is in a list
# param: headerList, a list containing commands for running this program
#        str, the section of the headerFile to be read
# return: the index of the line immediately following the specified section
def readHeader(headerList, section):
    index = 0
    for line in headerList:
        index += 1
        if line == section:
            return index
        
# Transposes a file and resets its index
# param: toTranspose, file which we want to transpose
# return: a file which has been transposed and had its index reset
def freshTranspose(toTranspose):
    transposed = toTranspose.transpose()
    transposed.reset_index(drop=True, inplace=True)
    return transposed



# extract filenames from header
with open(args.header) as headerFile:
    for line in headerFile:
        headerContent.append(line.strip()) 
        
#TODO: can make this more robust by finding "# INPUT FILES" and then grabbing filenames from that index
file012 = pd.read_csv(headerContent[indx012], sep='\t', header = None)

# remove any extensions from Indv TODO: (maybe make this an option in header)
noExt = ['locus']
with open(headerContent[indxIndv]) as indvExt:
    for line in indvExt:
        temp = line.split('.')
        noExt.append(temp[0])
fileIndv = pd.DataFrame({None:noExt})
#fileIndv = pd.read_csv(headerContent[indxIndv], sep='\t', header = None) TODO: keeping this until I can make it optional

# delete the index of the 012 file and transpose
file012 = file012.drop(file012.columns[0], axis = 1)
#file012T = file012.transpose()
#file012T.reset_index(drop=True, inplace=True)
file012T = freshTranspose(file012)

# replace tab with underscore in filePos 
filePos = pd.read_csv(headerContent[indxPos], sep='\n', header = None)
filePosUnder = filePos.replace(to_replace='\t', regex=True, value='_')

# make filePosUnder first column in file012T
file012T.insert(0, column=None, value=filePosUnder)
#temp = file012T.transpose()
#temp.reset_index(drop=True, inplace=True)
temp = freshTranspose(file012T)
file012T = temp.transpose()

# extract method from headerFile 
index = 0
for line in headerContent:
    index += 1
    if line == '# METHOD':
        method = headerContent[index]
        break

if method == 'Purcell':
    alphaFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'A', 'B', 'A'])
    alphaInverseFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'B', 'A', 'B'])
    combo = pd.concat([alphaFile, alphaInverseFile])
    combo.reset_index(drop=True, inplace=True)
elif method == 'Brelsford':
    alphaFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'A', 'B', 'B'])
    alphaInverseFile = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'B', 'A', 'A'])
    altAlpha = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'A', 'A', 'B'])
    altAlphaInverse = file012T.replace(to_replace=[-1, 0, 1, 2], value=['U', 'B', 'B', 'A'])
    combo = pd.concat([alphaFile, alphaInverseFile, altAlpha, altAlphaInverse])
    combo.reset_index(drop=True, inplace=True)
else:
    #TODO: throw error
    print('Please fill out # METHOD field in the header file')
    

# TODO: Make these optional if user doesn't want extension stripping
#fileIndvIns = pd.DataFrame([['locus']], columns=fileIndv.columns)
#fileIndv2 = pd.concat([fileIndvIns, fileIndv])
#fileIndv2.reset_index(drop=True, inplace=True)
#fileIndvT = fileIndv2.transpose()

# count rows and columns and instantiate numOfInd and numOfLoci respectively
numOfInd = combo.shape[1] - 1
numOfLoci = combo.shape[0]

# insert top row using transposed fileIndv
fileIndvT = fileIndv.transpose()
headerless = pd.concat([fileIndvT, combo])
headerless.reset_index(drop=True, inplace=True)

# extract MCTHeader TODO: make if statements finding loci and pop_num and adding them automatically
index = 0
MCTHeader = []
for line in headerContent:
    index += 1
    if line == '# MCT HEADER':
        while True:
            if index >= len(headerContent):
                break
            #tempList = headerContent[index].split()    might be usefull for forcing tab separation in MCTHeader 
            MCTHeader.append(headerContent[index] + '\n')
            index += 1

MCTHeader.append('number_of_loci' + '\t' + str(numOfLoci) + '\n')
MCTHeader.append('number_of_individual' + '\t' + str(numOfInd) + '\n')
MCTHeader.append('\n')

# write header and dataframe to file
with open(args.output, 'x') as toWrite:
    toWrite.writelines(MCTHeader)
toWrite.close()
headerless.to_csv(args.output, mode='a', sep='\t', header=None, index=None)     
#combo.to_csv(args.output, mode='a', sep='\t', header=None, index=None)