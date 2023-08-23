#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
#import re
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering out individuals with high proportions of missing data (VCF files)',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--debug', help='print debug output', action='store_true')
parser.add_argument('--input', help='file to read from')
parser.add_argument('--scaffs', help='list of scaffolds to extract/exclude')
parser.add_argument('--invert', help='extract all but named scaffold (y/n)', default='n')


## Global Variables

args = parser.parse_args()
output = args.input + ".scaffExtract"
scaffList = args.scaffs.split()

## Main

# Read input file, write header and all desired lines to file
with open(args.input, 'r') as file, open(output, 'w+') as outFile:
    for line in file:
        if args.invert == 'y':
            if line.split()[0] == "@SQ" or line.split()[0] == "@PG" or line.split()[2] not in scaffList:
                outFile.write(line)
        else:    
            if line.split()[0] == "@SQ" or line.split()[0] == "@PG" or line.split()[2] in scaffList:
                outFile.write(line)
    