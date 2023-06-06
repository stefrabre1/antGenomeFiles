from os import listdir
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# set up parser to accept command line arguments
parser = argparse.ArgumentParser(description='Creates scatter plots of plink files')
parser.add_argument('--input', help='file to be read')
parser.add_argument('--image', help='the type of scatterplot to be saved', default = "no_star")
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

# read file into a pandas dataframe
df = pd.read_csv(args.input, sep = ' ', header = None)

# delete column 1
df.drop(df.columns[0], axis=1, inplace = True)

# Read columns 1 and 2 into a scatterplot
x = df[2].astype(float)
y = df[3].astype(float)

# plot the first two information columns in a scatter
plt.scatter(x, y)
plt.grid()
imageName = args.input + '.png'

if args.image == "no_star":
    plt.savefig(imageName)

# find the mean of x and y
meanX = sum(abs(x))/len(x)
meanY = sum(abs(y))/len(y)

# create arrays for storing points we might want to delete
potentialDeleteX = []
potentialDeleteY = []
indArray = []

# plot points which are too far from the mean as seperate symbols
for i in range(len(x)):
    if abs(x[i]) > (meanX + 0.15):
        potentialDeleteX.append(x[i])
        potentialDeleteY.append(y[i])
        
        
        plt.plot(x[i], y[i], c = "red", marker = '*', markersize = 10)
        plt.text(x[i], y[i], df[1][i], fontsize = 9)
 
        indArray.append(i)
 
    elif abs(y[i]) > (meanY + 0.15):
        potentialDeleteX.append(x[i])
        potentialDeleteY.append(y[i])

        plt.plot(x[i], y[i], c = "red", marker = '*', markersize = 10)
        plt.text(x[i], y[i], df[1][i], fontsize = 9)

        indArray.append(i)

if args.image != "no_star":
    plt.savefig(imageName)

refined = False
# check with user if they want to delete points which were too far from the mean
for i in range(len(indArray)):
    distX = abs(potentialDeleteX[i]) - meanX
    distY = abs(potentialDeleteY[i]) - meanY

    totalDist = None
    if distX > distY:
        totalDist = distX
    else:
        totalDist = distY

    while True:
        prompt = "Would you like to delete " + df[1][i] + "? (distance from mean: " + str(round(totalDist, 2)) + ") (y/n): "
        answer = input(prompt)
        
        if not any(x in answer for x in ['y', 'n']):
            print("Please input a valid response. y = yes, n = no")
            continue
        else:
            break
            
    if answer == 'y':
        print("\nDeleting " + df[1][i] + "\n")
        df.drop(indArray[i], inplace = True)
        refined = True
    else:
        print("\nKeeping " + df[1][i] + "\n")
        
# write dataframe with deleted points to file.
if refined == True:
    output = args.input + ".refined"
    refinedFile = "Changes recorded to " + output
    print(refinedFile)
    df.to_csv(output, sep='\t', header=None, index=None)
    
    x2 = df[2].astype(float)
    y2 = df[3].astype(float)
    plt.clf()
    plt.scatter(x2, y2)
    plt.grid()
    refImage = args.input + ".refined.png" 
    refinedPng = "Updated scatterplot image is labeled: " + refImage
    print(refinedPng)
    plt.savefig(refImage)
else:
    notRefined = "No changes made to " + args.input
    print(notRefined)

    