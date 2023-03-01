#!/usr/bin/python3

# script for filtering poorly sequenced individuals 

import os
import re
from os import listdir
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for isolating allele counts below a certain threshold',
    epilog="Good Luck with Your Bioinformatics!")
parser.add_argument('--input', help='file to read data from')
parser.add_argument('--threshold', help='count of homogeneous alleles to isolate', default='1')
parser.add_argument('--debug', help='print debug output', action="store_true")

## Global variables

args = parser.parse_args()
THRESH = int(args.threshold)
ALLELE_COL = 2
HOM1 = 0
HOM2 = 2

## Functions

# Gets the nth column in a line and returns it as an int value
# param: value, a line containing three columns separated by slashes
#        n, an integer indicating the column to isolate
# return: an integer which represents homogenous, heterogenous, or alternate allele count 
def getAlleleCount(value, n):
    return int(value.split('/')[n])
    
# Isolates the nth column from a delimited text file 
# param: line, a line read from a file
#        n, the column to be isolated
# return: a string containing the nth column of a line in a delimited text file
def getColumn(line, n):
    return str(line.split()[n])
    
# Determines if an allele count is at or below threshold
# param: hom, an integer representing homogeneous allele counts
# return: a boolean value, true if hom is at or below threshold and not equal to zero
def atOrBelow(hom):
    return hom <= THRESH and hom != 0 
    
# compares checks if either homogeneous allele is at or below threshold
# param: line, a line read from a file
# return: aboolean value, false if neither allele is below threshold, true if either is below
def homThreshold(line):
    column = getColumn(line, ALLELE_COL)
    firstHom = getAlleleCount(column, HOM1)
    secondHom = getAlleleCount(column, HOM2)
    
    if atOrBelow(firstHom) or atOrBelow(secondHom):
        return True
    else:
        return False
    
# writes the first three columns to a file if hetero allele is above threshold or either homo allele is 0 or 1
# param: line, a line read from a file
#        file, the file containing data above threshold
def badDataToFile(line, file):
    
    if homThreshold(line):
        lineToWrite = getColumn(line, 0) + '\t' + getColumn(line, 1) + '\t' + getColumn(line, 2) + '\n'
        file.write(lineToWrite)

## Main

# TODO: change the name of this project
# Welcome the user and indicate the thresholds being used
print("The badScaffsToFile.py script has launched!")

# Read the file containing allele frequency data and write bad lines to a seperate file
with open(args.input, 'r') as a_file:
    
    # TODO: DON'T KEEP THIS HARD CODED
    badSnps = open('badScaffs.txt', 'w+')
    for line in a_file:
    
        if getColumn(line, 0) != 'CHR':
            badDataToFile(line, badSnps)
    badSnps.close()

# Indicate the end of file processing
print("All done!")