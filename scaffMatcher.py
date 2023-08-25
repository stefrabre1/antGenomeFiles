#!/usr/bin/python3

# script for filtering out individuals with high proportions of missing data (VCF files)

import os
import argparse
from difflib import SequenceMatcher

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering out individuals with high proportions of missing data (VCF files)',
    epilog="Good Luck with Your Bioinformatics! This script is written and directed by Daniela Zarate PHD")
parser.add_argument('--debug', help='print debug output', action='store_true')
parser.add_argument('--input1', help='file to read from')
parser.add_argument('--input2', help='file to read from')

## Global Variables

args = parser.parse_args()
output1 = args.input1 + ".scaffsMatched"
output2 = args.input2 + ".scaffsMatched"

## Main

#remove all header content from file 2
with open(args.input2, 'r') as file, open("temp", 'w+') as out:
    for line in file:
        if line.split()[0] != "@SQ" or line.split()[0] != "@PG":
            out.write(line)

# find matching data between the two files and output to corresponding files
with open(args.input1, 'r') as inFile1, open("temp", 'r') as inFile2, open(output1, 'w+') as outFile1, open(output2, 'w+') as outFile2:
    file2 = inFile2.readlines()
    for line in inFile1:
        if "c29.sm_sm.rep" in line:
            outFile1.write(line)
            
        tempLine = line.split()[0].strip()
        
        for line2 in file2:             
            if tempLine == line2.split()[0].strip():                
                outFile1.write(line)
                outFile2.write(line2)
    
os.remove("temp")

with open (output1, 'r') as inFile, open("uniqueGenes", 'w+') as outFile:
    file = inFile.readlines()
    output = []
    count = 0
    
    for line in file:
        col1 = line.split()[0] + '\n'
        if col1 not in output and col1.find('.') == -1:
            count += 1
            output.append(col1)
    outFile.writelines(output)
    print("The number of unique genes is: " + str(count))