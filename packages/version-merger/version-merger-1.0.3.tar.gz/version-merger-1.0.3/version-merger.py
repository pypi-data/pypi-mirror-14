#!/usr/bin/env python

import subprocess
import time
import shutil
import os
import glob
import argparse

parser = argparse.ArgumentParser(description="Run version merger")
parser.add_argument("-i", "--input", metavar="filename", required=True, type=str, help="Input file to version merge")
parser.add_argument("-o", "--output", metavar="filename", default="master.csv", type=str, help="Output file to version merge")
parser.add_argument("-t", "--time", metavar="seconds", default=60, type=int, help="Time interval between each merge")
parser.add_argument("-r", "--resolution", metavar="seconds", default=5, type=int, help="Time interval between each snapshot (stash)")
args = parser.parse_args()

inputFile = args.input
outputFile = args.output
timeInterval = args.time
dataResolution = args.resolution

def stash(name_of_file):
    shutil.copy(name_of_file, './clone.csv')
    subprocess.call('git add clone.csv', shell=True)
    subprocess.call('git stash', shell=True)
    print 'Submitted'
    time.sleep(dataResolution)

def startGit():
    fileClone = open('clone.csv', 'w+')
    fileClone.close
    subprocess.call('git init', shell=True)
    subprocess.call('git config --global user.email "you@example.com"', shell=True)
    subprocess.call('git config --global user.name "Your Name"', shell=True)
    subprocess.call('git add clone.csv', shell=True)
    subprocess.call('git commit -m "First Commit"', shell=True)

#A substring is chosen for the script to stop the loop once it reaches the end of git stash list
def file(name_of_file):
    string_for_file_script = 'cat %s temp%stemp.csv > temp%soutput.csv' % (name_of_file, name_of_file, name_of_file)
    string_for_convert_script = 'cat temp%soutput.csv > temp%stemp.csv' % (name_of_file, name_of_file)
    subprocess.call(string_for_file_script, shell=True)
    subprocess.call(string_for_convert_script, shell=True)

# A function to start version control for n seconds
def versionControl(second_delay, name_of_file):
    t_end = time.time() + second_delay
    while time.time() < t_end:
        newest = max(glob.iglob(name_of_file), key=os.path.getctime)
        stash(newest)
        print newest

# A function for Git to change the stash
def runGit(): 
    subprocess.call('git reset --hard', shell=True) 
    subprocess.call('git stash pop -q', shell=True)
    print 'Done'
    
# A function to copy to a MASTER copy
def createCopy(name_of_output_file):
    for jl in glob.glob("*temp.csv"):
	os.remove(jl)
    createMaster = 'cat *output.csv >> %s' % name_of_output_file
    subprocess.call(createMaster, shell=True)
    for kl in glob.glob("*output.csv"):
	os.remove(kl)

# A function to merge all the version control
def unPop():
    while True:
    	substring = 'stash@{0}:'
    	outputfromList = subprocess.check_output('git stash list', shell=True)
    	if substring in outputfromList:
	    runGit()
	    for abc in glob.glob("clone*.csv"):
   		file(abc)
	else:	
	    createCopy(outputFile)
	    break

# Main command that creates a blank copy called 'clone.csv'
if __name__=="__main__":
    try:
        startGit()
        while True:
            versionControl(timeInterval, inputFile)
            unPop()
    except IOError:
        pass
