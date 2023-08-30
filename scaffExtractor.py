#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for extracting specified scaffolds from a file',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--input', help='file to read from')
parser.add_argument('--output', help='file to write to', default = "extractedScaffs")
parser.add_argument('--scaffFile', help='a file containing a list of scaffolds to extract/exclude')
parser.add_argument('--debug', help='print debug output', action='store_true')

## Global Variables

args = parser.parse_args()

scaffList = []
with open (args.scaffFile, 'r') as file:
    for line in file:
        scaffList.append(line.strip())
        
#test 
print(scaffList)

## Main

# Read input file, write header and all desired lines to file
with open(args.input, 'r') as file, open(args.output, 'w+') as outFile:
    for line in file:
        if line.split()[0] == "@SQ" or line.split()[0] == "@PG" or line.split()[2] in scaffList:
            outFile.write(line)
    