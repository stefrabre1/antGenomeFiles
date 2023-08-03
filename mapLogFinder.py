import os
import argparse
from pathlib import Path

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Makes the start and end bin counts continuous accross chromosomes')
parser.add_argument('--input', help='directory to be searched')
parser.add_argument('--output', help='output file', default = 'mapLogData.txt')
parser.add_argument('--debug', help='print debug output', action='store_true')
args = parser.parse_args()

# Global variables
FILE_EXT = ".mapLog.final.out"
INPUT = args.input + "/"
LINE_AND_VALUE = 5

# main
filelist = os.listdir(INPUT)
toFile = []

for i in filelist:
    if i.endswith(FILE_EXT):
        
        fullFileName = str(Path(i).stem)
        fileName = fullFileName.split('.')[0]
        
        with open(INPUT + i, 'r') as f:
            content = f.readlines()
            inputReads = content[LINE_AND_VALUE].split()[LINE_AND_VALUE]
            
            #test
            #print(inputReads)
            
            strToFile = fileName + '\t' + inputReads + '\n'
            toFile.append(strToFile)    
            
with open(args.output, 'w+') as out:
    for line in toFile:
        out.write(line)