#!/usr/bin/python3

# script for filtering assembled and unassembled alignments generated from ddRADseq demultiplexing data 

import os
import re
from os import listdir
import argparse
import numpy

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering assembled and unassembled alignments generated from ddRADseq demultiplexing data',
    epilog="Good Luck with Your Bioinformatics!")
parser.add_argument('--vcfFile', help='the VCF file to be modified')
parser.add_argument('--badScaffolds', help='the file containing bad scaffolds')
parser.add_argument('--output', help='the filtered VCF file', default='filteredVCF.vcf')
parser.add_argument('--debug', help='print debug output', action="store_true")

## Global variables

args = parser.parse_args()
BAD_SCAFFS = []
HOM1 = '0/0'
HOM2 = '1/1'
FIX = './.'

## Functions

# Determines if the first or second homogeneous allele is below or at threshold
# param: line, a line from a file of scaffolds
# return: an int value, 1 if the first allele is at or below threshold, 2 if the second allele is, -1 if neither
def hom1Or2(line):
    if int(str(line.split()[2]).split('/')[0]) == 1:
        return 1
    elif int(str(line.split()[2]).split('/')[2]) == 1:
        return 2
    return -1

# Determines if a line contains bad data by checking against a list 
# param: aList, represents a list of known scaffolds with bad data
#        aKey, the scaffold we're checking against the bad data list
# return: an int value, 1 the first allele is 1, 2 if the second is 1, 0 if neither is 1
def checkBadLine(scaff, aList):
    for line in aList:
        key = line.split()[0] + '\t' + line.split()[1]
        if (scaff.startswith(key)):
            return hom1Or2(line)
    return 0
    
# Replaces the bad data associated with the scaffold name with './.'
# param: line, a line containing scaffold data
#        allele, an int value indicating which allele the bad data was associated with
# return: a string containing all the corrected data
def replaceBadData(line, allele):   
    if allele == 1:
        return line.replace(HOM1, FIX)
    else:
        return line.replace(HOM2, FIX)
    
# Splits lines read from file into a list, searches for specified values in said list, then writes lines to file if the line contains AS and XS values within threshold
# param: line, a line read from a file
#        aList, a list containing the names of bad scaffolds to check for
#        temp, a file which lines are written to if they fit the specified parameters
def processLine(line, aList, file):
    checkedLine = checkBadLine(line, aList)
    
    if checkedLine == 0:
        file.write(line)
    elif checkedLine == 1:
        file.write(replaceBadData(line, checkedLine))
    elif checkedLine == 2:
        file.write(replaceBadData(line, checkedLine))
    else:
        print("Whoops!")

## Main

# Welcome the user :)
print("The fixVcfFile.py script has launched!")

# read in bad scaffolds from text file and remove any newline characters
with open(args.badScaffolds, 'r') as badScaffs:
    BAD_SCAFFS = badScaffs.read().splitlines()

with open(args.vcfFile, 'r') as a_file:
    filtered = open(args.output, 'w+')
    
    for line in a_file:
        
        if not line.startswith('Scaffold'):
            filtered.write(line)
        else:
            processLine(line, BAD_SCAFFS, filtered)
    filtered.close()