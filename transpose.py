#!/usr/bin/python3

# an itty bitty script to transpose columns and rows of a file 

from os import listdir
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Transposes rows to columns in a text file.')
parser.add_argument('--input', help='filename input')
parser.add_argument('--output', help='filename for the shell script', default="out.sh")
parser.add_argument('--deleteIndex', help='deletes the first column of the file (y/n)', default="y")
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# read the file names 
poly  = pd.read_csv(args.input, sep = "\t", header = None) 

# delete the first column of the delimited file (index)
if args.deleteIndex == "y":
    poly = poly.drop(poly.columns[0], axis = 1)
    print("\nIndex deleted")
else:
    print("\nIndex kept")

# transpose rows and columns
print("Transposing the data set")
df = poly.transpose()
df.to_csv(args.output, sep = "\t", header = None, index = None) 

# close the file 

