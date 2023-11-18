"""A script which batch merges compressed fastq files together"""
import argparse
import subprocess

### Global variables

### Functions

def get_args() -> argparse.Namespace:
    """Gets command line arguments

    :return: arguments input by user in the command line
    :rtype: argparce.Namespace 
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--fileA',
        type=str,
        help='Input the path to the first list of files to be merged'
    )    
    parser.add_argument(
        '--fileB',
        type=str,
        help='Input the path to the second list of files to be merged'
    )
    args = parser.parse_args()
    return args

### Main

with open(get_args().fileA, 'r') as fileA, open(get_args().fileB, 'r') as fileB:
    ## read both files line by line
    for lineA, lineB in zip(fileA, fileB):
        ## run a BASH command to merge the files
        cmd = "gzcat " + lineA + " " + lineB + " " + lineA.split('.')[0] + "_merged.gz"
        subprocess.run(cmd)