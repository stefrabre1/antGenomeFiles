"""Read specific stdout files containing statistical data and extracts from them"""
import os
from pathlib import Path

## Global variables
FILE_EXT = ".stdout"
DIR = "./"
AMOUNT = 4
STAT = 5

filelist = os.listdir(DIR)
toFile = []

## Main

for file in filelist:
    if file.endswith(FILE_EXT):
    
        fullFileName = str(Path(file).stem)
        fileName = fullFileName.split('.')[0] + fullFileName.split('.')[1] + '\t'
        amountToFile = ""
        statToFile = ""
        
        with open(DIR + file, 'r') as f:
            for line in f:
                if 'Surviving:' in line:
                    amountToFile = line.split()[AMOUNT] + '\t'
                    statToFile = line.split()[STAT].replace('(', '').replace(')', '') + '\n'

        toFile.append(fileName + amountToFile + statToFile)    

amountSum = 0
statSum = 0
count = 0
for line in toFile:
    count += 1
    amountSum += int(line.split('\t')[1])
    statSum += float(line.split('\t')[2].replace('%', '').strip())
    
print("The average survival rate is of reads: " + str(statSum/count) + "%\n" + "The total number of survivor reads is: " + str(amountSum))
           
with open('trimmedStats.txt', 'w+') as out:
    for line in toFile:
        out.write(line)