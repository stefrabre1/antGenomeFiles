#!/usr/bin/python3

# script for filtering assembled and unassembled alignments generated from ddRADseq demultiplexing data 

import os
import re
from os import listdir
import argparse
import numpy

# Set up a very helpful argument parser ecosystem to read in arguments passed through on the command line
parser = argparse.ArgumentParser(
    description='script for filtering assembled and unassembled alignments generated from ddRADseq demultiplexing data',
    epilog="Good Luck with Your Bioinformatics!")
parser.add_argument('--outputdir', help='directory to write files to', default='filteredSam')
parser.add_argument('--path', help='directory to read files from', default=".")
parser.add_argument('--minAS', help='minimum quality threshold score to filter for (INT)', type=int, default="-12")
parser.add_argument('--maxXS', help='maximum duplication allowed (INT)', default="-25")
parser.add_argument('--debug', help='print debug output', action="store_true")

## Global variables

args = parser.parse_args()
MIN_AS=int(args.minAS)
MAX_XS=int(args.maxXS)

## Functions

# Gets the third column in a line and returns it as an int value
# param: value, a line containing three columns separated by colons
# return: an integer which represents either an AS or XS value
def getFieldInt(value):
    return int(value.split(':')[2])

# Determines if an AS value is properly formated (three columns, seperated by colons) and that the AS value is above threshold
# param: val, a string representing an AS value
# return: boolean, true if AS value is properly formated AND above threshold, false otherwise
def asOverMin(val):
    return val.startswith('AS:i:') and getFieldInt(val) > MIN_AS

# Determines if an XS value is properly formated (three columns, seperated by colons) and that the XS value is below threshold
# param: val, a string representing an XS value
# return: boolean, true if XS value is properly formated AND below threshold, false otherwise
def xsUnderMax(val):
    return val.startswith('XS:i:') and getFieldInt(val) < MAX_XS

# Finds the specified column by searching for aKey in aList 
# param: aList, represents a row in a delimited file
#        aKey, the specified string to find in a row
# return: c, the string in a row which we wanted to find (AS or XS value)
def getKeyEntryFromList(aList, aKey):
    for c in aList:
        if (c.startswith(aKey)):
            return c
    print( "key %s not found", format(aKey))
    print(aList)
    sys.exit("quitting due to missing key")
    
# Splits lines read from file into a list, searches for specified values in said list, then writes lines to file if the line contains AS and XS values within threshold
# param: line, a line read from a file
#        temp, a file which lines are written to if they fit the specified parameters
def processLine(line, temp):
    row = line.split()
    
    as_value = getKeyEntryFromList(row, "AS")
    xs_value = getKeyEntryFromList(row, "XS")

    if ( asOverMin(as_value) and xsUnderMax(xs_value) ):
        temp.write(line)

# Creates lists containing all AS and XS values 
# param: line, a line read from file
#        ASList, a list to be populated with all AS values
#        XSList, a list to be populated with all XS values
def buildLists(line, ASList, XSList):
    row = line.split()
   
    as_value = getKeyEntryFromList(row, "AS")
    xs_value = getKeyEntryFromList(row, "XS")
    
    ASList.append(getFieldInt(as_value))
    XSList.append(getFieldInt(xs_value))

# Finds the average of a list above a threshold and below it, if there are no values to average then an average of 0 is returned
# param: list, a list of AS or XS values
#        threshold, a user specified threshold 
# return: toReturn, a tuple with the first index being the average below threshold, and the second tuple being the average above
def averageAboveAndBelow(list, threshold):
    above = []
    below = []
    toReturn = []
    
    for value in list:
        if value > threshold:
            above.append(value)
        else:
            below.append(value)
            
    if len(below) > 0:
        toReturn.append(numpy.average(below))
    else:
        toReturn.append(0)
    
    if len(above) > 0:
        toReturn.append(numpy.average(above))
    else:
        toReturn.append(0)
    
    return toReturn

# Counts the number of AS or XS values above a user specified threshold
# param: list, a list of AS or XS values
#        threshold, a threshold set by the user
# return: count, the number of values above the specified threshold   
def countAbove(list, threshold):
    count = 0
    
    for value in list:
        if value > threshold:
            count += 1
    return count

# Prints statistical data about AS and XS values to stdout and to file
# param: ASList, a list containing all AS values
#        XSList, a list containing all XS values
#        file, an output file for all statistical data to be written to
def printAndWrite(ASList, XSList, file):
    lineToPrint = "The smallest AS value is: " + str(min(ASList)) + "\n" \
                  + "The smallest XS value is: " + str(min(XSList)) + "\n" \
                  + "The largest AS value is: " + str(max(ASList)) + "\n" \
                  + "The largest XS value is: " + str(max(XSList)) + "\n" \
                  + "The average AS value below threshold is: " + str(averageAboveAndBelow(ASList, MIN_AS)[0]) + "\n" \
                  + "The average AS value above threshold is: " + str(averageAboveAndBelow(ASList, MIN_AS)[1]) + "\n" \
                  + "The average XS value below threshold is: " + str(averageAboveAndBelow(XSList, MAX_XS)[0]) + "\n" \
                  + "The average XS value above threshold is: " + str(averageAboveAndBelow(XSList, MAX_XS)[1]) + "\n" \
                  + "The overall average of AS is: " + str(numpy.average(ASList)) + "\n" \
                  + "The overall average of XS is: " + str(numpy.average(XSList)) + "\n" \
                  + "The total number of AS values above threshold are: " + str(countAbove(ASList, MIN_AS)) + "\n" \
                  + "The total number of AS values below threshold are: " + str((len(ASList) - countAbove(ASList, MIN_AS))) + "\n" \
                  + "The total number of XS values above threshold are: " + str(countAbove(XSList, MAX_XS)) + "\n" \
                  + "The total number of XS values below threshold are: " + str((len(XSList) - countAbove(XSList, MAX_XS))) + "\n"

    print(lineToPrint)
    file.write(lineToPrint)
    file.close()

## Main

# Welcome the user :)
print("The alignment.filter.py script has launched!")

# Change the directory to the working directory, passed through from the command line
os.chdir(args.path)

print("The working directory is: %s" % os.getcwd())
print("The minimum alignment score threshold (AS) is: %d" % MIN_AS)
print("The maximum alignment score threshold for the second-best alignment (XS) is: %d" % MAX_XS)

# make a directory to output the filtered reads, using the output name provided in command line argument --outputdir
os.mkdir(args.outputdir)
print("Directory \"%s\" created for filtered alignments" % args.outputdir)

# Read the file containing raw AS and XS data, use functions to write data within parameters to another file and process statistical data
for doc in os.listdir(args.path):

    if doc.endswith('tester.txt'):
        filter = os.path.join(args.outputdir, doc)
        stats = os.path.join(args.outputdir, "stats.txt")
        unfiltered = os.path.join(args.path, doc)
        ASList = []
        XSList = []
        temp = open(filter, 'w+')
        statsFile = open(stats, 'w+')
        with open(unfiltered, 'r') as a_file:

            for line in a_file:
                if line.startswith('@'):
                    temp.write(line)
                else:
                    processLine(line, temp)
                    buildLists(line, ASList, XSList)
            temp.close()
        printAndWrite(ASList, XSList, statsFile)