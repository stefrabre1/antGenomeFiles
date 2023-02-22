#!/usr/bin/python3

# script for filtering poorly sequenced individuals 

import os
import re
from os import listdir
import argparse
import numpy

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering poorly sequenced individuals',
    epilog="Good Luck with Your Bioinformatics!")
parser.add_argument('--output', help='file to write data to', default='badSNPs.txt')
parser.add_argument('--input', help='file to read data from')
parser.add_argument('--het', help='percentage threshold for heterozygous data (FLOAT)', default='0.05')
parser.add_argument('--debug', help='print debug output', action="store_true")

## Global variables

args = parser.parse_args()
HET_THRESHOLD = float(args.het)
ALLELE_COL = 2
HOM1 = 0
HET = 1
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
    
# compares heterogenous allele count to the summation of all alleles and checks if it's above a certain threshold
# param: line, a line read from a file
# return: a boolean value, true if above threshold, false if below
def hetAboveThreshold(line):
    column = getColumn(line, ALLELE_COL)
    firstHom = getAlleleCount(column, HOM1)
    hetero = getAlleleCount(column, HET)
    secondHom = getAlleleCount(column, HOM2)
    
    return hetero > HET_THRESHOLD * (firstHom + hetero + secondHom)
    
# determines if homogeneous alleles 1 and 2 are 0 or 1
# param: line, a line read from a file
# return: a boolean value, true if either homogeneous allele is 0 or 1
def homoZeroOrOne(line):
    column = getColumn(line, ALLELE_COL)
    firstHom = getAlleleCount(column, HOM1)
    secondHom = getAlleleCount(column, HOM2)

    return (firstHom * secondHom) < (firstHom + secondHom)

# writes the first three columns to a file if hetero allele is above threshold or either homo allele is 0 or 1
# param: line, a line read from a file
#        file, the file containing data above threshold
def badDataToFile(line, file):
    
    if hetAboveThreshold(line) and homoZeroOrOne(line):
        lineToWrite = getColumn(line, 0) + '\t' + getColumn(line, 1) + '\t' + getColumn(line, 2) + '\n'
        file.write(lineToWrite)

## Main

# Welcome the user and indicate the thresholds being used
print("The hardy-weinberg-filter.py script has launched!")
print("The heterogenous threshold is %.2f" % HET_THRESHOLD)

# Read the file containing allele frequency data and write bad lines to a seperate file
with open(args.input, 'r') as a_file:
    
    badSnps = open(args.output, 'w+')
    for line in a_file:
    
        if getColumn(line, 0) != 'CHR':
            badDataToFile(line, badSnps)
    badSnps.close()

# Indicate the end of file processing
print("All done!")