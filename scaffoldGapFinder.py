#!/usr/bin/python3

# an itty bitty script to find the differences between scaffolds

from os import listdir
import argparse

parser = argparse.ArgumentParser(description='find the difference between genetic scaffolds and save ones above certain thresholds')
parser.add_argument('--input', help='filename for the input file')
parser.add_argument('--output', help='filename for the output file', default="out")
parser.add_argument('--threshold', help='only extract values strictly greater than the threshold')
parser.add_argument('--moderate', help='define what is a moderate difference between scaffolds')
parser.add_argument('--severe', help='define what is a severe difference between scaffolds')
parser.add_argument('--debug', help='print debug output', action="store_true")
args = parser.parse_args()

aboveTInd = []
scaffsAboveT = []
moderateScaffs = []
severeScaffs = []
index1 = 0
index2 = 0
index3 = 0

# open the file, find all indices above a certain threshold, and save them
with open(args.input) as f1: 
	content = f1.readlines()
	tempList = content[2].split()	
	
	# store the index of every linkage group above threshold
	for i in tempList:
		if i.isnumeric():
			if int(i) > int(args.threshold):
				aboveTInd.append(index1)
			index1 += 1				

# find lines where scaffolds above threshold start and calculate the difference between adjacent scaffolds 
	for i in content:
		
		# end loop if there are no more linkage groups above threshold
		if (index3 >= len(aboveTInd)):
			break
		
		# find groups above threshold 
		strToComp = "group lg" + str(aboveTInd[index3])
		if strToComp in i:
			
			# magic number
			j = 2
			
			# iterate through linkage group and compare adjacent scaffolds
			while True:
				scaff1 = content[index2 + j].split()
				scaff2 = content[index2 + j + 1].split()	
				
				# end loop once terminus is reached
				if scaff2[0] == ";ENDOFGROUP":
					break 		
				diff = float(scaff2[1]) - float(scaff1[1])
				if diff > float(args.severe):
					severe = "There is a severe difference between " + scaff1[0] + " and " + scaff2[0] + " and that is: " + str(diff)
					print(severe)
					severeScaffs.append(severe)
				elif diff > float(args.moderate):
					moderate = "There is a moderate difference between " + scaff1[0] + " and " + scaff2[0] + " and that is: " + str(diff)
					print(moderate)	
					moderateScaffs.append(moderate)
				j += 1
			index3 += 1
		index2 += 1

# close the file
f1.close()

# write severeScaffs and moderateScaffs to log
with open(args.output, "x") as toWrite:
	toWrite.write("The severe differences are:\n")	
	for i in severeScaffs:
		toWrite.write(i)
		toWrite.write("\n")
	toWrite.write("\nThe moderate differences are:\n")
	for i in moderateScaffs:
		toWrite.write(i)
		toWrite.write("\n")

# close the file 
toWrite.close()