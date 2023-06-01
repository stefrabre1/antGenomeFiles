#!/usr/bin/python3

# script for matching allele frequencies between individuals 

import os
import re
from os import listdir
import argparse

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='Hello! I am a python script used for identifying loci that share congruent paternal ancestry between subfamilies of worker ants',
    epilog="Good Luck with Your Bioinformatics!")
parser.add_argument('--input', help='file to read data from')
parser.add_argument('--debug', help='print debug output', action="store_true")

## Global variables

args = parser.parse_args()
ALLELE_COL1 = 2
ALLELE_COL2 = 5
ALLELE_COL3 = 8
HOM1 = 0
HET = 1
HOM2 = 2

## Functions

# Gets the nth column in a line and returns it as an int value
# param: value, a line containing three columns separated by slashes
#        n, an integer indicating the column to isolate
# return: an integer which represents homogenous, heterogenous, or alternate allele count 
def getAlleleCount(value, n):
    if value is not None:
        return int(value.split('/')[n])
    
# Isolates the nth column from a delimited text file 
# param: line, a line read from a file
#        n, the column to be isolated
# return: a string containing the nth column of a line in a delimited text file
def getColumn(line, n):
        return str(line.split()[n])

# Tests alleles from two different scaffolds to catagorize their types
# param: alleleList, a list of values representing homozygous and heterozygous counts for alleles 2 and 3
# return: an integer from 0-8, 1-8 representing that type n is true, 0 if false
def typeTests(alleleList):
    # Type 1 A2: #/#/0  A3: #/#/0
    if alleleList[0] != 0 and alleleList[1] != 0 and alleleList[2] == 0 and alleleList[3] != 0 and alleleList[4] != 0 and alleleList[5] == 0:
        return 1
    # Type 2 A2: 0/#/#  A3: 0/#/#
    if alleleList[0] == 0 and alleleList[1] != 0 and alleleList[2] != 0 and alleleList[3] == 0 and alleleList[4] != 0 and alleleList[5] != 0:
        return 2
    # Type 3 A2: #/#/0  A3: 0/#/#
    if alleleList[0] != 0 and alleleList[1] != 0 and alleleList[2] == 0 and alleleList[3] == 0 and alleleList[4] != 0 and alleleList[5] != 0:
        return 3
    # Type 4 A2: #/#/0  A3: #/0/0
    if alleleList[0] != 0 and alleleList[1] != 0 and alleleList[2] == 0 and alleleList[3] != 0 and alleleList[4] == 0 and alleleList[5] == 0:
        return 4
    # Type 5 A2: 0/#/#  A3: #/0/0
    if alleleList[0] == 0 and alleleList[1] != 0 and alleleList[2] != 0 and alleleList[3] != 0 and alleleList[4] == 0 and alleleList[5] == 0:
        return 5
    # Type 6 A2: #/#/#  A3: 0/0/#
    if alleleList[0] != 0 and alleleList[1] != 0 and alleleList[2] != 0 and alleleList[3] == 0 and alleleList[4] == 0 and alleleList[5] != 0:
        return 6
    # Type 7 A2: 0/#/#  A3: 0/#/0
    if alleleList[0] == 0 and alleleList[1] != 0 and alleleList[2] != 0 and alleleList[3] == 0 and alleleList[4] != 0 and alleleList[5] == 0:
        return 7
    # Type 8 A2: #/#/0  A3: 0/#/0
    if alleleList[0] != 0 and alleleList[1] != 0 and alleleList[2] == 0 and alleleList[3] == 0 and alleleList[4] != 0 and alleleList[5] == 0:
        return 8
    else:
        return 0

# Tests if the relationship between scaffolds is type 1 (meaning that ALLELE2 is #/#/0 and ALLELE3 is #/#/0)
# param: line, a line from the file of scaffolds
#        n, an integer representing a value between 1-8 
# return: a boolean value, True if the relationship is type 1, false otherwise
def typeN(line, n):
    allele2 = getColumn(line, ALLELE_COL2)
    hom1A2 = getAlleleCount(allele2, HOM1)
    hetA2 = getAlleleCount(allele2, HET)
    hom2A2 = getAlleleCount(allele2, HOM2)

    allele3 = getColumn(line, ALLELE_COL3)
    hom1A3 = getAlleleCount(allele3, HOM1)
    hetA3 = getAlleleCount(allele3, HET)
    hom2A3 = getAlleleCount(allele3, HOM2)

    alleleList = [hom1A2, hetA2, hom2A2, hom1A3, hetA3, hom2A3]

    return (typeTests(alleleList) == n)
    
# writes all nine columns to a file if firstHom = 0 in all individuals
# param: line, a line read from a file
#        typeList, a list of integers representing the test types
#        fileList, a list of files to be written to
def typeToFile(line, typeList, fileList):
    for n in range(len(typeList)):        
        if typeN(line, typeList[n]):
            fileList[n].write(line)

# records overall type count
# param: line, a line read from a file
#        countList, a list of integers representing the number of different allele relationships in the file
def recordTypes(line, countList):
    allele2 = getColumn(line, ALLELE_COL2)
    hom1A2 = getAlleleCount(allele2, HOM1)
    hetA2 = getAlleleCount(allele2, HET)
    hom2A2 = getAlleleCount(allele2, HOM2)

    allele3 = getColumn(line, ALLELE_COL3)
    hom1A3 = getAlleleCount(allele3, HOM1)
    hetA3 = getAlleleCount(allele3, HET)
    hom2A3 = getAlleleCount(allele3, HOM2)

    alleleList = [hom1A2, hetA2, hom2A2, hom1A3, hetA3, hom2A3]

    n = typeTests(alleleList) - 1

    if typeTests(alleleList) != -1:
        countList[n] += 1

# prints the overall type counts to terminal and writes them to a file
# param: countList, a list of integers representing the number of different allele relationships in the file
def printAndWriteStats(countList):
    statsFile = open('commonFatherSNPsStats.txt', 'w+')
    for i in range(len(countList)):
        output = "The number of type" + str(i+1) + " relationships is: " + str(countList[i]) + "\n"
        print(output)
        statsFile.write(output)
    
    statsFile.close()
    
## Main

# Welcome the user and indicate the thresholds being used
print("The fatherMatcher.py script has launched!")

# Read the file containing allele frequency data and write allele types to appropriate files
with open(args.input, 'r') as a_file:    
# Prompt user to select which types should be printed to file
    goodInput = False
    while goodInput == False:
        errorFlag = False
        prompt = "Please input a list of types which you'd like written to file \n(IE: 1 2 5 8 This would create 4 files for type1, type2, type5, and type8): "
        answer = input(prompt)
        
        typeList = []            
        for i in answer.split():
            if int(i) not in [1, 2, 3, 4, 5, 6, 7, 8] or int(i) in typeList:
                print("Please input a valid type. Should be integers between 1-8 seperated by a space\nThere shouldn't be any duplicate types input\n")
                typeList = []
                errorFlag = True
                break
            else:
                typeList.append(int(i))
                
        if errorFlag == False:
            goodInput = True
        
    # Create output files for allele types
    fileList = []
    for i in typeList:
        fileName = 'commonFatherSNPsType' + str(i) + '.txt'
        typeFile = open(fileName, 'w+')
        fileList.append(typeFile)
    
    # create list which will record the number of each type is present in the file
    countList = [0, 0, 0, 0, 0, 0, 0, 0]
    
    # read file and process data
    for line in a_file:
        if getColumn(line, 0) != 'CHR':
            typeToFile(line, typeList, fileList)
            recordTypes(line, countList)
    
    # print overall information to terminal and file
    printAndWriteStats(countList)
    
    # close type files
    for i in fileList:
        i.close()

# Indicate the end of file processing
endnote = "Loci that have congruent patterns of paternal inheritance between subfamilies \n have been written to the files commonFatherSNPsType#.txt. \n Use this file to select only these loci for further downstream analyis."
print(endnote)
