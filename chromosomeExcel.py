from os import listdir
import argparse
import pandas as pd

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Creates scatter plots of plink files')
parser.add_argument('--input', help='file to be read')
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# Global variables
CHROME_START = 1
COL_DIST = 4
SPACER = 50
SCAFF_START = 4

# read file into a pandas dataframe and create a new dataframe to write changes to
df = pd.read_csv(args.input, skiprows = 2, sep='\t', header = None, names = range(108))
newDf = pd.DataFrame()

chromeSum = 0

#[TODO I'm fucking lost, this is terrible]
# Read columns starting at column 2 and skipping over 4 at a time
for i in range(CHROME_START, len(df.columns), COL_DIST):
    pd.to_numeric(df[i])
    df.dropna(subset=[i], inplace = True)
    df[i] += chromeSum
    chromeSum = df[i].iloc[-1] + SPACER

    tempDf = pd.DataFrame()
    tempDf.insert(0, 0, df[i], True)

    newDf = newDf.append(tempDf)
    newDf.reset_index()
    
output = args.input + ".condensed"
newDf.to_csv(output, sep='\t', header=None, index=None)
    