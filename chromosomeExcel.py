from os import listdir
import argparse
import pandas as pd
import csv

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Creates scatter plots of plink files')
parser.add_argument('--input', help='file to be read')
parser.add_argument('--num_col', help='number of columns in file')
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# Global variables
NUM_COL = int(args.num_col)
CHROME_START = 1
COL_DIST = 4
SPACER = 50
SCAFF_START = 3

# read file and remove null characters
# with open(args.input, "r") as data:
#     new = data.read().decode('utf-16-le')
    

# read file into a pandas dataframe and create a new dataframe to write changes to

# shitty xlsx file
#df = pd.read_csv(args.input, skiprows = 2, encoding = 'UTF-8', sep="\\", header = None, names = range(NUM_COL))

# not shitty text file
df = pd.read_csv(args.input, skiprows = 2, sep='\t', header = None, names = range(NUM_COL))
newDfChrome = pd.DataFrame()
newDfScaff = pd.DataFrame()

chromeSum = 0

# Read columns starting at column 2 and skipping over 4 at a time
for i in range(CHROME_START, len(df.columns), COL_DIST):
    tempDf = pd.DataFrame()
    tempDf[0] = df[i]
    tempDf.dropna(subset=[0], inplace = True)
    tempDf[0] = tempDf[0].astype(float)
    #pd.to_numeric(df[i])
    tempDf[0] += chromeSum
    chromeSum = tempDf[0].iloc[-1] + SPACER

    newDfChrome = newDfChrome.append(tempDf)

scaffSum = 0

# Read columns starting at column 4 and skipping over 4 at a time
for j in range(SCAFF_START, len(df.columns), COL_DIST):
    tempDf = pd.DataFrame()
    tempDf[0] = df[j]
    tempDf.dropna(subset=[0], inplace = True)
    splitDf = pd.DataFrame()
    tempDf[0] = tempDf[0].astype(str).str.split('p', 1).str[1]
    tempDf[0] = tempDf[0].astype(int) 
    tempDf[0] += scaffSum
    scaffSum = tempDf[0].iloc[-1] + SPACER

    newDfScaff = newDfScaff.append(tempDf)

newDfChrome.reset_index(inplace = True, drop = True)
newDfScaff.reset_index(inplace = True, drop = True)
toOut = pd.concat([newDfChrome, newDfScaff], axis=1)
    
output = args.input + ".condensed"
toOut.to_csv(output, sep='\t', header=None, index=None)
    