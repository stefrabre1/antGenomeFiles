from os import listdir
import argparse
import pandas as pd

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Makes the start and end bin counts continuous accross chromosomes')
parser.add_argument('--input', help='file to be read')
parser.add_argument('--debug', help='print debug output', action='store_true')
args = parser.parse_args()

# Global variables
BIN_START = 1
BIN_END = 2

# read file into a pandas dataframe and create new dataframe to write changes to
#df = pd.read_csv(args.input, skiprows = 1, sep='\t', header = None)
df = pd.read_csv(args.input, sep='\t')

df = df[~df.CHROM.str.contains("Contig") & ~df.CHROM.str.contains("Mito")]
df = df.sort_values(by = ['CHROM', 'BIN_START'])
df = df.reset_index(drop=True)

# variables for making continuous
beingBin = 0
endBin = 0
dfContBin = pd.DataFrame()
toAddStart = 0
toAddEnd = 0

# sort by position for each scaffold
while endBin < df.shape[0] - 1:
    tempDf = pd.DataFrame()
    sameBin = df.iat[endBin, 0]
    newBin = df.iat[endBin, 0]
    
    # find section of dataframe with all same chromosome numbers
    while sameBin == newBin:
  
        endBin += 1
        if endBin == df.shape[0]:
            break
        newBin = df.iat[endBin, 0]
           
    tempDf = df.loc[beingBin:(endBin-1)]
    beingBin = endBin

    tempDf = tempDf.copy()

    tempDf.loc[:, "BIN_START"] = tempDf.loc[:, "BIN_START"].add(toAddStart)
    tempDf.loc[:, "BIN_END"] = tempDf.loc[:, "BIN_END"].add(toAddEnd)
    
    toAddStart = tempDf.iat[-1, BIN_START]
    toAddEnd = tempDf.iat[-1, BIN_END]
        
    dfContBin = dfContBin.append(tempDf)

# output dataframe to file
output = args.input + ".continuous"
dfContBin.to_csv(output, sep='\t', index=None)