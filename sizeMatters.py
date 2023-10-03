"""Python script for scraping size metrics from bash ls -lh and printing summary stats"""
import os

## Global Variables

# the location of the file size in the array.
FILE_SIZE = 4

# counts for different sizes of files
less_five = 0
five_twenty = 0
twenty_fifty = 0
fifty_hundred = 0
above_hundred = 0

## Main

# list all files in current directory ending with .gz
cmd = 'ls -lh *.gz'
file_info = os.popen(cmd)

# iterate through all files listed
for line in file_info:
    # get the size of the file
    str_size = line.split()[FILE_SIZE]
    # cut the last character off the string and convert it to a numerical type
    num_size = float(str_size[:-1])

    # check the value of each file size and increment the appropriate counter
    if size[-1] == 'K' or num_size < 5:
        less_five += 1
    elif num_size >= 5 and num_size < 20:
        five_twenty += 1
    elif num_size >= 20 and num_size < 50:
        twenty_fifty += 1
    elif num_size >= 50 and num_size < 100:
        fifty_hundred += 1
    elif size[-1] == 'G' or num_size >= 100:
        above_hundred += 1

# create message for output 
message = "The number of 5M < files: " + str(less_five) + '\n'\
          "The number of 5M <= files < 20M : " + str(five_twenty) + '\n'\
          "The number of 20M <= files < 50M : " + str(twenty_fifty) + '\n'\
          "The number of 50M <= files < 100M : " + str(fifty_hundred) + '\n'\
          "The number of files >= 100M : " + str(above_hundred) + '\n'
          
print(message)