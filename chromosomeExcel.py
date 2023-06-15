from os import listdir
import argparse
import pandas as pd
import csv

# just playing
import matplotlib.pyplot as plt

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

# shitty xlsx file (NOT WORKING, NEED TO FIGURE OUT UNICODE-16 INPUT MY GOD)
#df = pd.read_csv(args.input, skiprows = 2, encoding = 'UTF-8', sep="\\", header = None, names = range(NUM_COL))

# not shitty text file
df = pd.read_csv(args.input, skiprows = 2, sep='\t', header = None, names = range(NUM_COL))
newDfChrome = pd.DataFrame()
newDfP = pd.DataFrame()
newDfScaff = pd.DataFrame()

chromeSum = 0

# add and increment chromosome column
for i in range(CHROME_START, len(df.columns), COL_DIST):
    tempDf = pd.DataFrame()
    tempDf[1] = df[i]
    tempDf.dropna(subset=[1], inplace = True)
    
    tempDf[1] = tempDf[1].astype(float)
    tempDf[1] += chromeSum
    chromeSum = tempDf[1].iloc[-1] + SPACER

    newDfChrome = newDfChrome.append(tempDf)

# add position column 
for j in range(SCAFF_START, len(df.columns), COL_DIST):
    tempDf2 = pd.DataFrame()
    tempDf2[2] = df[j]
    tempDf2.dropna(subset=[2], inplace = True)

    tempDf2[2] = tempDf2[2].astype(str).str.split('p', 1).str[1]
    tempDf2[2] = tempDf2[2].astype(int) 
    # tempDf2[2] += pSum
    # pSum = tempDf2[2].iloc[-1] + SPACER

    newDfP = newDfP.append(tempDf2)

# add scaffold column
for k in range(SCAFF_START, len(df.columns), COL_DIST):
    tempDf3 = pd.DataFrame()
    tempDf3[0] = df[k]
    tempDf3.dropna(subset=[0], inplace = True)

    tempDf3[0] = tempDf3[0].astype(str).str.split('p', 1).str[0]
    tempDf3[0] = tempDf3[0].astype(str).str.replace('c', 's')
    tempDf3[0] = tempDf3[0].astype(str).str.split('s', 1).str[1]
    tempDf3[0] = tempDf3[0].astype(int)

    newDfScaff = newDfScaff.append(tempDf3)
    
newDfChrome.reset_index(inplace = True, drop = True)
newDfP.reset_index(inplace = True, drop = True)
newDfScaff.reset_index(inplace = True, drop = True)

toSort = pd.concat([newDfScaff, newDfChrome, newDfP], axis=1)
sortedScaff = toSort.sort_values(by=[0])
sortedScaff.reset_index(inplace = True, drop = True)

beginScaff = 0
endScaff = 0
pSum = 0
sortedP = pd.DataFrame()

# sort by position for each scaffold
while endScaff < sortedScaff.shape[0] - 1:
    sameScaff = sortedScaff.iat[endScaff, 0]
    newScaff = sortedScaff.iat[endScaff, 0]
    
    while sameScaff == newScaff:
        endScaff += 1
        if endScaff == sortedScaff.shape[0] - 1:
            break
        newScaff = sortedScaff.iat[endScaff, 0]
        
    # if endScaff - beginScaff > -1:
        # tempDf4 = sortedScaff.loc[beginScaff:endScaff]
    # else:
        # continue
    
    tempDf4 = sortedScaff.loc[beginScaff:endScaff]
    
    beginScaff = endScaff + 1
    tempDf4 = tempDf4.sort_values(by=[2])

    tempDf4[2] += pSum    
    pSum = tempDf4[2].iloc[-1] + SPACER
    
    sortedP = sortedP.append(tempDf4)

# iterate through scaffs column row by row, counting how many of the same value there are
# Keep track of there a value ends, make a range from end of last scaffold to end of present scaffold
    # iloc[0:30], iloc[31:62] etc
# For each of these ranges, make a new dataframe from toSort 
# sort these individual dataframes by their position column
# append each dataframe to the last and 
    
output = args.input + ".condensed"
sortedP.to_csv(output, sep='\t', header=None, index=None)
    
# See the scatter

# Read columns 1 and 2 into a scatterplot
x = sortedP[1].astype(float)
y = sortedP[2].astype(float)
plt.clf()

# plot the first two information columns in a scatter
plt.scatter(x, y)
plt.grid()
#plt.show()
imageName = "lmaoScatter.png"
plt.savefig(imageName)
