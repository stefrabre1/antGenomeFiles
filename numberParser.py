#!/usr/bin/python3

# an itty bitty script to parse large numbers from a list in a file 

from os import listdir
import argparse

parser = argparse.ArgumentParser(description='Extract all numbers from a specific line of a file and save ones above a certain threshold to another file')
parser.add_argument('--input', help='filename for the input file')
parser.add_argument('--output', help='filename for the output file', default="out")
parser.add_argument('--lineNum', help='specify the line number which you want to extract numerical data from')
parser.add_argument('--threshold', help='only extract values strictly greater than the threshold')
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# open the file, find sepcified line and save said line to list
lst = []
with open(args.input) as f: 
	content = f.readlines()
	tempList = content[int(args.lineNum) - 1].split()	
	for i in tempList:
		if i.isnumeric():
			lst.append(int(i))

# write numbers above the threshold to file
aboveThresh = 0
with open(args.output, "x") as toWrite:
	for i in lst:
		if i > int(args.threshold):
			aboveThresh += 1
			toWrite.write(str(i))
			toWrite.write("\n")

# print out the amount of linkages above and below the threshold
belowThresh = len(lst) - aboveThresh
print("The number of linkage groups above the threshold is: ", aboveThresh)
print("The number of linkage groups below the threshold is: ", belowThresh)

# close the file 
toWrite.close()