#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
import argparse
from difflib import SequenceMatcher

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for finding matching scaffolds between two files and removing them',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--debug', help='print debug output', action='store_true')
parser.add_argument('--input1', help='file to read from')
parser.add_argument('--input2', help='file to read from')

## Global Variables

args = parser.parse_args()
output1 = args.input1 + ".scaffsRemoved"
output2 = args.input2 + ".scaffsRemoved"

## Main

# find matching data between the two files and output to corresponding files
with open(args.input1, 'r') as inFile1, open(args.input2, 'r') as inFile2, open(output1, 'w+') as outFile1, open(output2, 'w+') as outFile2:
    file2 = inFile2.readlines()
    for line in inFile1:
        tempLine = line.split()[0].strip()
        
        for line2 in file2:             
            if tempLine != line2.split()[0].strip():                
                outFile1.write(line)
                outFile2.write(line2)