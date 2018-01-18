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
#right arm stuff
psL1 = []
psL2 = []
psR1 = []
psR2 = []
sh1 = []
sh2 = []
sh3 = []
sh4 = []
sh5 = []
#left arm stuff
prl1L1 = []
prl1L2 = []
prl1R1 = []
prl1R2 = []
prl2L1 = []
prl2L2 = []
prl2R1 = []
prl2R2 = []

VDC = []

s0_done = False
s2L_done = False
s2R_done = False
gc_done = False
psL_done = False
psR_done = False
sh1_done = False
sh2_done = False
sh3_done = False
sh4_done = False
sh5_done = False
prl1L_done = False
prl1R_done = False
prl2L_done = False
prl2R_done = False
vdc_done = False

while i<(int(runnum)+1):
  try:
    if right_arm:
      halog_file = open("/adaqfs/home/adaq/epics/runfiles_tritium_R/halog_end_"+str(i)+".epics","r")
    else:
      halog_file = open("/adaqfs/home/adaq/epics/runfiles_tritium_L/halog_end_"+str(i)+".epics","r")
    found=True
  except IOError:
    found=False
  if found:
    run.append(i)
    for line in halog_file:
      if line.startswith('Set HV (V)'):
        if not s0_done:
          s0.append(float(line.split()[3])+float(line.split()[4]))
          s0_done = True
        elif not s2L_done:
          s2L1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10]))
          s2L2.append(float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18]))
          s2L_done = True
        elif not s2R_done:
          s2R1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10]))
          s2R2.append(float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18]))
          s2R_done = True
        elif not gc_done:
          gc.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12]))
          gc_done = True
        elif not psL_done and right_arm:
          psL1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14]))
          psL1.append(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
          psL_done = True
        elif not psR_done and right_arm:
          psR1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14]))
          psR1.append(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
          psR_done = True
        elif not sh1_done and right_arm:
          sh1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          sh1_done = True
        elif not sh2_done and right_arm:
          sh2.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          sh2_done = True
        elif not sh3_done and right_arm:
          sh3.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          sh3_done = True
        elif not sh4_done and right_arm:
          sh4.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          sh4_done = True
        elif not sh5_done and right_arm:
          sh5.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          sh5_done = True
        elif not prl1L_done and not right_arm:
          prl1L1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          prl1L2.append(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          prl1L_done = True
        elif not prl1R_done and not right_arm:
          prl1R1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          prl1R2.append(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          prl1R_done = True
        elif not prl2L_done and not right_arm:
          prl2L1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          prl2L2.append(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          prl2L_done = True
        elif not prl2R_done and not right_arm:
          prl2R1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          prl2R2.append(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          prl2R_done = True
        elif not vdc_done:
          VDC.append(float(line.split()[3])+float(line.split()[4]))
  i+=1
  s0_done = False
  s2L_done = False
  s2R_done = False
  gc_done = False
  psL_done = False
  psR_done = False
  sh1_done = False
  sh2_done = False
  sh3_done = False
  sh4_done = False
  sh5_done = False
  prl1L_done = False
  prl1R_done = False
  prl2L_done = False
  prl2R_done = False
  vdc_done = False
  halog_file.close()


print run
print s0
print s2L1
print s2R2
