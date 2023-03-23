#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
import re
from os import listdir
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering out individuals with high proportions of missing data (VCF files)',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--maxMISS', help='maximum percent of missing data (INT)', default="0.25")
parser.add_argument('--debug', help='print debug output', action="store_true")
parser.add_argument('--path', help='directory to read files from', default=".")

## Global Variables

args = parser.parse_args()
MAX_MISS=float(args.maxMISS)

## Functions

# Function to get MAX_MISS value 
# param: line, a line from a file
# return: the 5th column of a line from a file as a floating point
def getMaxMiss(line):
    return float(line.split()[4])

# Function to determine if data is over threshold
# param: line, a line from a file
# return: true if a value is above threshold, false if a value is less than or equal to the threshold
def maxMissOverMin(line):
        return getMaxMiss(line) > MAX_MISS

# Writes data below threshold to goodData file and data above to badData file
# param: line, a line from a file
#        good, a file containing all the lines which are above the threshold
#        bad, a file containing all the lines which are at or below threshold
#        badIndv, a file containing only the first column of all the lines which are at or below threshold
def measureMaxMiss(line, good, bad, badIndv):
    if ( maxMissOverMin(line) == True ):
        bad.write(line)
        badIndv.write(line.split()[0] + '\n')
    else:
        good.write(line)

## Main

# Welcome the user :)
print("The missingIndv.py script has launched!")

# Change the directory to the working directory, passed through from the command line
os.chdir(args.path)

# Inform the user of the threshold
print("The maximum percent of missing data allowed per individual is: %f" % MAX_MISS)

# Find imiss file, then parse data from it to goodData, badData, and badIndv files        
for doc in os.listdir(args.path):
    if doc.endswith('.imiss'):
        og_file = os.path.join(args.path, doc)
        good = open(os.path.join(args.path, str(doc) + ".goodData.txt"), 'w+')
        bad = open(os.path.join(args.path, str(doc) + ".badData.txt"), 'w+')
        badIndv = open(os.path.join(args.path, str(doc) + ".badIndv.txt"), 'w+')
        with open(og_file, 'r') as a_file:
            for line in a_file:
                # always write column headers to file
                if line.startswith('INDV'):
                    good.write(line)
                    bad.write(line)
                else:
                    measureMaxMiss(line, good, bad, badIndv)

            good.close()
            bad.close()
            badIndv.close()