#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
#import re
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering out individuals with high proportions of missing data (VCF files)',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--debug', help='print debug output', action="store_true")
parser.add_argument('--input', help='file to read from')

## Global Variables

args = parser.parse_args()

## Main

# Read input file, write header and all desired lines to file
with open(args.input, 'r') as file:
    output = args.input + ".scaffExtract"
    outFile = open(output, 'w+')
    for line in file:
        if line.split()[0] == "@SQ" or line.split()[0] == "@PQ" or line.split()[2] == "Scaffold03":
            outFile.write(line)
    
    outFile.close()