#!/usr/bin/python3

# an itty bitty script to convert certain numbers into letters in a file 

from os import listdir
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Convert numbers to letters (-1=U, 0=A, 1=B, and 2=A).')
parser.add_argument('--input', help='filename input')
parser.add_argument('--output', help='filename for the shell script', default="out.sh")
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# read the file names 
poly  = pd.read_csv(args.input, sep = "\t", header = None) 

# convert -1 to U, 0 to A, 1 to B, and 2 to A
for k in range(0,len(poly)):
	for j in poly.columns:
		if poly.loc[k][j] == "-1":
			poly.loc[k][j] = "U"
		elif poly.loc[k][j] == "0":
			poly.loc[k][j] = "A"
		elif poly.loc[k][j] == "1":
			poly.loc[k][j] = "B"
		elif poly.loc[k][j] == "2":
			poly.loc[k][j] = "A"
		else: 
			continue

# write duplicated dataframe to file
print("Successfully converted numbers to letters")
poly.to_csv(args.output, sep = "\t", header = None, index = None) 

# close the file 
