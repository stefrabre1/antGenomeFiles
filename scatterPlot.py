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
df = pd.read_csv(args.input, sep = '\t', header = None)

# Read columns 1 and 2 into a scatterplot
x = df[1]
y = df[2]

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
        plt.text(x[i], y[i], df[0][i], fontsize = 9)
 
        indArray.append(i)
 
    elif abs(y[i]) > (meanY + 0.15):
        potentialDeleteX.append(x[i])
        potentialDeleteY.append(y[i])

        plt.plot(x[i], y[i], c = "red", marker = '*', markersize = 10)
        plt.text(x[i], y[i], df[0][i], fontsize = 9)

        indArray.append(i)

# show the final plot
plt.show()

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
        prompt = "Would you like to delete " + df[0][i] + "? (distance from mean: " + str(round(totalDist, 2)) + ") (y/n): "
        answer = input(prompt)
        
        if not any(x in answer for x in ['y', 'n']):
            print("Please input a valid response. y = yes, n = no")
            continue
        else:
            break
            
    if answer == 'y':
        print("\nDeleting " + df[0][i] + "\n")
        df.drop(indArray[i], inplace = True)
        refined = True
    else:
        print("\nKeeping " + df[0][i] + "\n")
        
# write dataframe with deleted points to file.
if refined == True:
    output = args.input + ".refined"
    message1 = "Changes recorded to " + output
    print(message1)
    df.to_csv(output, sep='\t', header=None, index=None) 
else:
    message2 = "No changes made to " + args.input
    print(message2)

    