#!/usr/bin/python

###########################################################
# read-hv.py
# Reads in the high voltage history from halog files.
# Creates a ROOT script that plots and outputs a pdf
#
# Author: Tyler Hague
###########################################################

import sys
import string
import subprocess

if len(sys.argv)==2:
  if sys.argv[1]=='right':
    right_arm = True
  elif sys.argv[1]=='left':
    right_arm = False
  else:
    print 'The second argument must be \'right\' or \'left\''
    sys.exit(1)
else:
  print 'Please specify if the code is being run for \'right\' or \'left\''
  sys.exit(1)

#Read in the run number from the rcRunNumber file
try:
  if right_arm:
    runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumberR","r")
  else:
    runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumber","r")
  runnum = runnum_file.readline()
  runnum = runnum.rstrip() #Removes \n end of line character and any trailing whitespace. There shouldn't be any in this case, but just in case
  runnum_file.close()
except IOError:
  runnum = raw_input('The most current run number can\'t be located. What run number would you like to plot to? ')

if right_arm:
  i=90760
else:
  i=1208

run = []
s0 = []
s2L1 = []
s2L2 = []
s2R1 = []
s2R2 = []
gc = []
if right_arm:
  psL1 = []
  psL2 = []
  psR1 = []
  psR2 = []
  sh1 = []
  sh2 = []
  sh3 = []
  sh4 = []
  sh5 = []
else:
  prl1L1 = []
  prl1L2 = []
  prl1R1 = []
  prl1R2 = []
  prl2L1 = []
  prl2L2 = []
  prl2R1 = []
  prl2R2 = []
VDC = []

while i<(run_num+1):
  try:
    if right_arm:
      halog_file = open("/adaqfs/home/adaq/epics/runfiles_tritium_R/halog_end_"+i+".epics","r")
    else:
      halog_file = open("/adaqfs/home/adaq/epics/runfiles_tritium_L/halog_end_"+i+".epics","r")
    found=True
  except IOError:
    found=False
  if found:
    run.append(i)
    for line in halog_file:
      if line.startswith('Set HV (V)'):
        if not s0_done:
          s0.append(int(line.split()[4])+int(line.split()[5])+int(line.split()[6]))
          s0_done = True
        elif not s2L_done:
          s2L1.append(int(line.split()[4])+int(line.split()[5])+int(line.split()[6])+int(line.split()[7])+int(line.split()[8])+int(line.split()[9])+int(line.split()[10])+int(line.split()[11]))
          s2L2.append(int(line.split()[12])+int(line.split()[13])+int(line.split()[14])+int(line.split()[15])+int(line.split()[16])+int(line.split()[17])+int(line.split()[18])+int(line.split()[19]))
          s2L_done = True
        elif not s2R_done:
          s2R1.append(int(line.split()[4])+int(line.split()[5])+int(line.split()[6])+int(line.split()[7])+int(line.split()[8])+int(line.split()[9])+int(line.split()[10])+int(line.split()[11]))
          s2R2.append(int(line.split()[12])+int(line.split()[13])+int(line.split()[14])+int(line.split()[15])+int(line.split()[16])+int(line.split()[17])+int(line.split()[18])+int(line.split()[19]))
          s2R_done = True
        elif not gc_done:
          gc.append(int(line.split()[4])+int(line.split()[5])+int(line.split()[6])+int(line.split()[7])+int(line.split()[8])+int(line.split()[9])+int(line.split()[10])+int(line.split()[11])+int(line.split()[12])+int(line.split()[13]))
          gc_done = True
        if right_arm:
          if not psL_done:
            psL1.append(int(line.split()[4]+int(line.splits()[5])+int(line.splits()[6])+int(line.splits()[7])+int(line.splits()[8])+int(line.splits()[9])+int(line.splits()[10])+int(line.splits()[11])+int(line.splits()[12])+int(line.splits()[13])+int(line.splits()[14])+int(line.splits()[15])
            psL1.append(int(line.split()[16]+int(line.splits()[17])+int(line.splits()[18])+int(line.splits()[19])+int(line.splits()[20])+int(line.splits()[21])+int(line.splits()[22])+int(line.splits()[23])+int(line.splits()[24])+int(line.splits()[25])+int(line.splits()[26])+int(line.splits()[27])
            psL_done = True
          if not psR_done:
            psR1.append(int(line.split()[4]+int(line.splits()[5])+int(line.splits()[6])+int(line.splits()[7])+int(line.splits()[8])+int(line.splits()[9])+int(line.splits()[10])+int(line.splits()[11])+int(line.splits()[12])+int(line.splits()[13])+int(line.splits()[14])+int(line.splits()[15])
            psR1.append(int(line.split()[16]+int(line.splits()[17])+int(line.splits()[18])+int(line.splits()[19])+int(line.splits()[20])+int(line.splits()[21])+int(line.splits()[22])+int(line.splits()[23])+int(line.splits()[24])+int(line.splits()[25])+int(line.splits()[26])+int(line.splits()[27])
            psR_done = True
  i+=1
