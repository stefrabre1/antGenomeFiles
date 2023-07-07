from os import listdir
import argparse
import pandas as pd
import csv

# just playing
import matplotlib.pyplot as plt

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Creates scatter plots of plink files')
parser.add_argument('--input', help='file to be read')
parser.add_argument('--scaff_thresh', help='threshold for the size of scaffolds', default='25')
parser.add_argument('--debug', help='print debug output', action='store_true')
args = parser.parse_args()

# Global variables
HALD_START = 1
COL_DIST = 4
SPACER = 50
SCAFF_START = 3
SCAFF_THRESH = int(args.scaff_thresh)

# read file into a pandas dataframe and create new dataframes to write changes to
df = pd.read_excel(args.input, skiprows = 2, header = None)
dfScaff = pd.DataFrame()
dfHald = pd.DataFrame()
dfPos = pd.DataFrame()

# drop columns with all NaN
df = df.dropna(axis = 1, how = 'all')

# add scaffold column
for i in range(SCAFF_START, len(df.columns), COL_DIST):
    tempDf1 = pd.DataFrame()
    tempDf1[0] = df[i]
    tempDf1.dropna(subset=[0], inplace = True)

    tempDf1[0] = tempDf1[0].astype(str).str.split('p', 1).str[0]
    tempDf1[0] = tempDf1[0].astype(str).str.replace('c', 's')
    tempDf1[0] = tempDf1[0].astype(str).str.split('s', 1).str[1]
    tempDf1[0] = tempDf1[0].astype(int)

    dfScaff = dfScaff.append(tempDf1)

# add Haldane distance column
haldSum = 0

for i in range(HALD_START, len(df.columns), COL_DIST):
    tempDf2 = pd.DataFrame()
    tempDf2[1] = df[i]
    tempDf2.dropna(subset=[1], inplace = True)
    
    tempDf2[1] = tempDf2[1].astype(float)
    tempDf2[1] += haldSum
    haldSum = tempDf2[1].iloc[-1] + SPACER

    dfHald = dfHald.append(tempDf2)

# add position column 
posSum = 0

for i in range(SCAFF_START, len(df.columns), COL_DIST):
    tempDf3 = pd.DataFrame()
    tempDf3[2] = df[i]
    tempDf3.dropna(subset=[2], inplace = True)

    tempDf3[2] = tempDf3[2].astype(str).str.split('p', 1).str[1]
    tempDf3[2] = tempDf3[2].astype(int) 
    
    tempDf3[2] += posSum
    posSum = tempDf3[2].iloc[-1] + SPACER

    dfPos = dfPos.append(tempDf3)
   
# reset indices for pandas sake   
dfHald.reset_index(inplace = True, drop = True)
dfPos.reset_index(inplace = True, drop = True)
dfScaff.reset_index(inplace = True, drop = True)

# sort all rows by scaffold 
toSort = pd.concat([dfScaff, dfHald, dfPos], axis=1)
sortedScaff = toSort.sort_values(by=[0])
sortedScaff.reset_index(inplace = True, drop = True)

# HAND CODED TEST, DO NOT USE
# # Remove scaffolds which may not have good data (TEST, might want to have user define threshold for number of scaffs instead and remove any below said number)
# badScaffs = [1, 3, 5, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 69, 70, 71, 72, 74, 75, 76, 78, 79, 80, 82, 84, 85, 86, 87, 90, 91, 92, 93, 94, 96, 99, 100, 102, 108, 109, 110, 111, 116, 121, 123, 127, 129, 133, 141, 143, 149, 156, 159, 183, 187, 189]

# if badScaffs is not None:
    # for i in badScaffs:
        # sortedScaff = sortedScaff[sortedScaff[0] != i]

# sortedScaff.reset_index(inplace = True, drop = True)

beginScaff = 0
endScaff = 0
pSum = 0
sortedP = pd.DataFrame()
x = []
y = []
l = 0

fig = plt.gcf()
fig.set_size_inches(20, 20)
fig.set_dpi(400)
plt.grid()

# sort by position for each scaffold
while endScaff < sortedScaff.shape[0] - 1:
    sameScaff = sortedScaff.iat[endScaff, 0]
    newScaff = sortedScaff.iat[endScaff, 0]
    
    while sameScaff == newScaff:
        endScaff += 1
        if endScaff == sortedScaff.shape[0]:
            break
        newScaff = sortedScaff.iat[endScaff, 0]
           
    tempDf4 = sortedScaff.loc[beginScaff:(endScaff-1)]
    
    if tempDf4.shape[0] >= SCAFF_THRESH:
        #test
        print(tempDf4.shape[0])
    
        beginScaff = endScaff 
        tempDf4 = tempDf4.sort_values(by=[2])

        tempDf4[2] += pSum    
        pSum = tempDf4[2].iloc[-1] + SPACER

        x = tempDf4[1].astype(float)
        y = tempDf4[2].astype(float)
        messageStart = "Scaff #" + str(sameScaff) + " start"
        messageEnd = "Scaff #" + str(sameScaff) + " end"
    
        if x is not None and y is not None:
            plt.text(x.iat[0], y.iat[0], messageStart, fontsize = 9, c = "blue") 
            plt.text(x.iat[-1], y.iat[-1], messageEnd, fontsize = 9, c = "red")
    
        plt.scatter(x, y)
    
        sortedP = sortedP.append(tempDf4)

imageName = args.input + ".scatter.png"
plt.savefig(imageName)
    
output = args.input + ".condensed"
sortedP.to_csv(output, sep='\t', header=None, index=None)