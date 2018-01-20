#!/usr/bin/python

###########################################################
# read-hv.py
# Reads in the high voltage history from halog files.
# Creates a ROOT script that plots and outputs a pdf
#
# Author: Tyler Hague
###########################################################

import sys
import os
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
  start_run = 90760
  i=90760
  arm = "RHRS"
else:
  start_run = 1208
  i=1208
  arm = "LHRS"

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

first_file = True
sets0_done = False
sets2L_done = False
sets2R_done = False
setgc_done = False
setpsL_done = False
setpsR_done = False
setsh1_done = False
setsh2_done = False
setsh3_done = False
setsh4_done = False
setsh5_done = False
setprl1L_done = False
setprl1R_done = False
setprl2L_done = False
setprl2R_done = False
setvdc_done = False

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
#In the first file, record the set hv so that for normalizing HV to 1
      if line.startswith('Set HV (V)') and first_file:
        if not sets0_done:
          sets0=(float(line.split()[3])+float(line.split()[4]))
          sets0_done = True
        elif not sets2L_done:
          sets2L1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10]))
          sets2L2=(float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18]))
          sets2L_done = True
        elif not sets2R_done:
          sets2R1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10]))
          sets2R2=(float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18]))
          sets2R_done = True
        elif not setgc_done:
          setgc=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12]))
          setgc_done = True
        elif not setpsL_done and right_arm:
          setpsL1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14]))
          setpsL2=(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
          setpsL_done = True
        elif not setpsR_done and right_arm:
          setpsR1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14]))
          setpsR2=(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
          setpsR_done = True
        elif not setsh1_done and right_arm:
          setsh1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          setsh1_done = True
        elif not setsh2_done and right_arm:
          setsh2=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          setsh2_done = True
        elif not setsh3_done and right_arm:
          setsh3=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          setsh3_done = True
        elif not setsh4_done and right_arm:
          setsh4=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          setsh4_done = True
        elif not setsh5_done and right_arm:
          setsh5=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17]))
          setsh5_done = True
        elif not setprl1L_done and not right_arm:
          setprl1L1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          setprl1L2=(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          setprl1L_done = True
        elif not setprl1R_done and not right_arm:
          setprl1R1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          setprl1R2=(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          setprl1R_done = True
        elif not setprl2L_done and not right_arm:
          setprl2L1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          setprl2L2=(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          setprl2L_done = True
        elif not setprl2R_done and not right_arm:
          setprl2R1=(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11]))
          setprl2R2=(float(line.split()[12])+float(line.split()[13])+float(line.split()[14])+float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19]))
          setprl2R_done = True
        elif not setvdc_done:
          setVDC=(float(line.split()[3])+float(line.split()[4]))
          setvdc_done = True

      if line.startswith('Read HV (V)'):
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
          psL2.append(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
          psL_done = True
        elif not psR_done and right_arm:
          psR1.append(float(line.split()[3])+float(line.split()[4])+float(line.split()[5])+float(line.split()[6])+float(line.split()[7])+float(line.split()[8])+float(line.split()[9])+float(line.split()[10])+float(line.split()[11])+float(line.split()[12])+float(line.split()[13])+float(line.split()[14]))
          psR2.append(float(line.split()[15])+float(line.split()[16])+float(line.split()[17])+float(line.split()[18])+float(line.split()[19])+float(line.split()[20])+float(line.split()[21])+float(line.split()[22])+float(line.split()[23])+float(line.split()[24])+float(line.split()[25])+float(line.split()[26]))
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
          vdc_done = True
  i+=1
  first_file = False
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

#ok. now to create a C file for making plots

try:
  os.remove("hv_plots.C")
except OSError:
  pass

plots = open("hv_plots.C","w+")

plots.write("void hv_plots(){\n")

i = 1
#Form the arrays
x = "double x[" + str(len(run)) + "] = {" + str(run[0]) + '\n'
ars0 = "double s0[" + str(len(run)) + "] = {" + str(s0[0]/sets0) + '\n'
ars2L1 = "double s2L1[" + str(len(run)) + "] = {" + str(s2L1[0]/sets2L1) + '\n'
ars2L2 = "double s2L2[" + str(len(run)) + "] = {" + str(s2L2[0]/sets2L2) + '\n'
ars2R1 = "double s2R1[" + str(len(run)) + "] = {" + str(s2R1[0]/sets2R1) + '\n'
ars2R2 = "double s2R2[" + str(len(run)) + "] = {" + str(s2R2[0]/sets2R2) + '\n'
argc = "double gc[" + str(len(run)) + "] = {" + str(gc[0]/setgc) + '\n'
arvdc = "double vdc[" + str(len(run)) + "] = {" + str(VDC[0]/setVDC) + '\n'
if right_arm:
  arpsL1 = "double psL1[" + str(len(run)) + "] = {" + str(psL1[0]/setpsL1) + '\n'
  arpsL2 = "double psL2[" + str(len(run)) + "] = {" + str(psL2[0]/setpsL2) + '\n'
  arpsR1 = "double psR1[" + str(len(run)) + "] = {" + str(psR1[0]/setpsR1) + '\n'
  arpsR2 = "double psR2[" + str(len(run)) + "] = {" + str(psR2[0]/setpsR2) + '\n'
  arsh1 = "double sh1[" + str(len(run)) + "] = {" + str(sh1[0]/setsh1) + '\n'
  arsh2 = "double sh2[" + str(len(run)) + "] = {" + str(sh2[0]/setsh2) + '\n'
  arsh3 = "double sh3[" + str(len(run)) + "] = {" + str(sh3[0]/setsh3) + '\n'
  arsh4 = "double sh4[" + str(len(run)) + "] = {" + str(sh4[0]/setsh4) + '\n'
  arsh5 = "double sh5[" + str(len(run)) + "] = {" + str(sh5[0]/setsh5) + '\n'
else:
  arprl1L1 = "double prl1L1[" + str(len(run)) + "] = {" + str(prl1L1[0]/setprl1L1) + '\n'
  arprl1L2 = "double prl1L2[" + str(len(run)) + "] = {" + str(prl1L2[0]/setprl1L2) + '\n'
  arprl1R1 = "double prl1R1[" + str(len(run)) + "] = {" + str(prl1R1[0]/setprl1R1) + '\n'
  arprl1R2 = "double prl1R2[" + str(len(run)) + "] = {" + str(prl1R2[0]/setprl1R2) + '\n'
  arprl2L1 = "double prl2L1[" + str(len(run)) + "] = {" + str(prl2L1[0]/setprl2L1) + '\n'
  arprl2L2 = "double prl2L2[" + str(len(run)) + "] = {" + str(prl2L2[0]/setprl2L2) + '\n'
  arprl2R1 = "double prl2R1[" + str(len(run)) + "] = {" + str(prl2R1[0]/setprl2R1) + '\n'
  arprl2R2 = "double prl2R2[" + str(len(run)) + "] = {" + str(prl2R2[0]/setprl2R2) + '\n'
while i<len(run):
  x += ", " + str(run[i]) + '\n'
  ars0 += ", " + str(s0[i]/sets0) + '\n'
  ars2L1 += ", " + str(s2L1[i]/sets2L1) + '\n'
  ars2L2 += ", " + str(s2L2[i]/sets2L2) + '\n'
  ars2R1 += ", " + str(s2R1[i]/sets2R1) + '\n'
  ars2R2 += ", " + str(s2R2[i]/sets2R2) + '\n'
  argc += ", " + str(gc[i]/setgc) + '\n'
  arvdc += ", " + str(VDC[i]/setVDC) + '\n'
#right arm stuff
  if right_arm:
    arpsL1 += ", " + str(psL1[i]/setpsL1) + '\n'
    arpsL2 += ", " + str(psL2[i]/setpsL2) + '\n'
    arpsR1 += ", " + str(psR1[i]/setpsR1) + '\n'
    arpsR2 += ", " + str(psR2[i]/setpsR2) + '\n'
    arsh1 += ", " + str(sh1[i]/setsh1) + '\n'
    arsh2 += ", " + str(sh2[i]/setsh2) + '\n'
    arsh3 += ", " + str(sh3[i]/setsh3) + '\n'
    arsh4 += ", " + str(sh4[i]/setsh4) + '\n'
    arsh5 += ", " + str(sh5[i]/setsh5) + '\n'
#left arm stuff
  else:
    arprl1L1 += ", " + str(prl1L1[i]/setprl1L1) + '\n'
    arprl1L2 += ", " + str(prl1L2[i]/setprl1L2) + '\n'
    arprl1R1 += ", " + str(prl1R1[i]/setprl1R1) + '\n'
    arprl1R2 += ", " + str(prl1R2[i]/setprl1R2) + '\n'
    arprl2L1 += ", " + str(prl2L1[i]/setprl2L1) + '\n'
    arprl2L2 += ", " + str(prl2L2[i]/setprl2L2) + '\n'
    arprl2R1 += ", " + str(prl2R1[i]/setprl2R1) + '\n'
    arprl2R2 += ", " + str(prl2R2[i]/setprl2R2) + '\n'
  i += 1
x += '};\n'
ars0 += '};\n'
ars2L1 += '};\n'
ars2L2 += '};\n'
ars2R1 += '};\n'
ars2R2 += '};\n'
argc += '};\n'
arvdc += '};\n'
#right arm stuff
if right_arm:
  arpsL1 += '};\n'
  arpsL2 += '};\n'
  arpsR1 += '};\n'
  arpsR2 += '};\n'
  arsh1 += '};\n'
  arsh2 += '};\n'
  arsh3 += '};\n'
  arsh4 += '};\n'
  arsh5 += '};\n'
#left arm stuff
else:
  arprl1L1 += '};\n'
  arprl1L2 += '};\n'
  arprl1R1 += '};\n'
  arprl1R2 += '};\n'
  arprl2L1 += '};\n'
  arprl2L2 += '};\n'
  arprl2R1 += '};\n'
  arprl2R2 += '};\n'

plots.write("TCanvas* s0gc = new TCanvas(\"s0gc\",\"s0 and gc\");\n")
plots.write("s0gc->Divide(2,1);\n")
plots.write("TCanvas* s2c = new TCanvas(\"s2c\",\"s2 Canvas\");\n")
plots.write("s2c->Divide(2,2);\n")
plots.write("TCanvas* calo1 = new TCanvas(\"calo1\",\"First Calorimeter\");\n")
plots.write("TCanvas* calo2 = new TCanvas(\"calo2\",\"Second Calorimeter\");\n")
plots.write("TCanvas* vdcc = new TCanvas(\"vdcc\",\"VDC Canvas\");\n")
plots.write(x)
plots.write(ars0)
plots.write("TGraph* s0g = new TGraph(" + str(len(run)) + ", x, s0);\n")
plots.write("s0g->SetTitle(\""+arm+" s0 HV sum\");\n")
plots.write("s0g->SetMaximum(" + str(1.1) + ");\n")
plots.write("s0g->SetMinimum(" + str(0.9) + ");\n")
plots.write("s0gc->cd(1);\ns0g->Draw(\"APL*\");\n")
plots.write(ars2L1)
plots.write("TGraph* s2L1g = new TGraph(" + str(len(run)) + ", x, s2L1);\n")
plots.write("s2L1g->SetTitle(\""+arm+" s2L First Half HV sum\");\n")
plots.write("s2L1g->SetMaximum(" + str(1.1) + ");\n")
plots.write("s2L1g->SetMinimum(" + str(0.9) + ");\n")
plots.write("s2c->cd(1);\ns2L1g->Draw(\"APL*\");\n")
plots.write(ars2L2)
plots.write("TGraph* s2L2g = new TGraph(" + str(len(run)) + ", x, s2L2);\n")
plots.write("s2L2g->SetTitle(\""+arm+" s2L Second Half HV sum\");\n")
plots.write("s2L2g->SetMaximum(" + str(1.1) + ");\n")
plots.write("s2L2g->SetMinimum(" + str(0.9) + ");\n")
plots.write("s2c->cd(2);\ns2L2g->Draw(\"APL*\");\n")
plots.write(ars2R1)
plots.write("TGraph* s2R1g = new TGraph(" + str(len(run)) + ", x, s2R1);\n")
plots.write("s2R1g->SetTitle(\""+arm+" s2R First Half HV sum\");\n")
plots.write("s2R1g->SetMaximum(" + str(1.1) + ");\n")
plots.write("s2R1g->SetMinimum(" + str(0.9) + ");\n")
plots.write("s2c->cd(3);\ns2R1g->Draw(\"APL*\");\n")
plots.write(ars2R2)
plots.write("TGraph* s2R2g = new TGraph(" + str(len(run)) + ", x, s2R2);\n")
plots.write("s2R2g->SetTitle(\""+arm+" s2R Second Half HV sum\");\n")
plots.write("s2R2g->SetMaximum(" + str(1.1) + ");\n")
plots.write("s2R2g->SetMinimum(" + str(0.9) + ");\n")
plots.write("s2c->cd(4);\ns2R2g->Draw(\"APL*\");\n")
plots.write(argc)
plots.write("TGraph* gcg = new TGraph(" + str(len(run)) + ", x, gc);\n")
plots.write("gcg->SetTitle(\""+arm+" Cherenkov HV sum\");\n")
plots.write("gcg->SetMaximum(" + str(1.1) + ");\n")
plots.write("gcg->SetMinimum(" + str(0.9) + ");\n")
plots.write("s0gc->cd(2);\ngcg->Draw(\"APL*\");\n")
#right arm stuff
if right_arm:
  plots.write("calo1->Divide(2,2);\n")
  plots.write("calo2->Divide(2,3);\n")
  plots.write(arpsL1)
  plots.write("TGraph* psL1g = new TGraph(" + str(len(run)) + ", x, psL1);\n")
  plots.write("psL1g->SetTitle(\""+arm+" Preshower Left First Half HV sum\");\n")
  plots.write("psL1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("psL1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(1);\npsL1g->Draw(\"APL*\");\n")
  plots.write(arpsL2)
  plots.write("TGraph* psL2g = new TGraph(" + str(len(run)) + ", x, psL2);\n")
  plots.write("psL2g->SetTitle(\""+arm+" Preshower Left Second Half HV sum\");\n")
  plots.write("psL2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("psL2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(2);\npsL2g->Draw(\"APL*\");\n")
  plots.write(arpsR1)
  plots.write("TGraph* psR1g = new TGraph(" + str(len(run)) + ", x, psR1);\n")
  plots.write("psR1g->SetTitle(\""+arm+" Preshower Right First Half HV sum\");\n")
  plots.write("psR1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("psR1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(3);\npsR1g->Draw(\"APL*\");\n")
  plots.write(arpsR2)
  plots.write("TGraph* psR2g = new TGraph(" + str(len(run)) + ", x, psR2);\n")
  plots.write("psR2g->SetTitle(\""+arm+" Preshower Right Second Half HV sum\");\n")
  plots.write("psR2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("psR2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(4);\npsR2g->Draw(\"APL*\");\n")
  plots.write(arsh1)
  plots.write("TGraph* sh1g = new TGraph(" + str(len(run)) + ", x, sh1);\n")
  plots.write("sh1g->SetTitle(\""+arm+" Shower Row 1 HV sum\");\n")
  plots.write("sh1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("sh1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(1);\nsh1g->Draw(\"APL*\");")
  plots.write(arsh2)
  plots.write("TGraph* sh2g = new TGraph(" + str(len(run)) + ", x, sh2);\n")
  plots.write("sh2g->SetTitle(\""+arm+" Shower Row 2 HV sum\");\n")
  plots.write("sh2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("sh2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(2);\nsh2g->Draw(\"APL*\");")
  plots.write(arsh3)
  plots.write("TGraph* sh3g = new TGraph(" + str(len(run)) + ", x, sh3);\n")
  plots.write("sh3g->SetTitle(\""+arm+" Shower Row 3 HV sum\");\n")
  plots.write("sh3g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("sh3g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(3);\nsh3g->Draw(\"APL*\");")
  plots.write(arsh4)
  plots.write("TGraph* sh4g = new TGraph(" + str(len(run)) + ", x, sh4);\n")
  plots.write("sh4g->SetTitle(\""+arm+" Shower Row 4 HV sum\");\n")
  plots.write("sh4g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("sh4g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(4);\nsh4g->Draw(\"APL*\");")
  plots.write(arsh5)
  plots.write("TGraph* sh5g = new TGraph(" + str(len(run)) + ", x, sh5);\n")
  plots.write("sh5g->SetTitle(\""+arm+" Shower Row 5 HV sum\");\n")
  plots.write("sh5g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("sh5g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(5);\nsh5g->Draw(\"APL*\");")
#left arm stuff
else:
  plots.write("calo1->Divide(2,2);")
  plots.write("calo2->Divide(2,2);")
  plots.write(arprl1L1)
  plots.write("TGraph* prl1L1g = new TGraph(" + str(len(run)) + ", x, prl1L1);\n")
  plots.write("prl1L1g->SetTitle(\""+arm+" Pion Rejector 1 Left First Half HV sum\");\n")
  plots.write("prl1L1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl1L1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(1);\nprl1L1g->Draw(\"APL*\");\n")
  plots.write(arprl1L2)
  plots.write("TGraph* prl1L2g = new TGraph(" + str(len(run)) + ", x, prl1L2);\n")
  plots.write("prl1L2g->SetTitle(\""+arm+" Pion Rejector 1 Left Second Half sum\");\n")
  plots.write("prl1L2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl1L2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(2);\nprl1L2g->Draw(\"APL*\");\n")
  plots.write(arprl1R1)
  plots.write("TGraph* prl1R1g = new TGraph(" + str(len(run)) + ", x, prl1R1);\n")
  plots.write("prl1R1g->SetTitle(\""+arm+" Pion Rejector 1 Right First Half HV sum\");\n")
  plots.write("prl1R1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl1R1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(3);\nprl1R1g->Draw(\"APL*\");\n")
  plots.write(arprl1R2)
  plots.write("TGraph* prl1R2g = new TGraph(" + str(len(run)) + ", x, prl1R2);\n")
  plots.write("prl1R2g->SetTitle(\""+arm+" Pion Rejector 1 Right Second Half HV sum\");\n")
  plots.write("prl1R2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl1R2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo1->cd(4);\nprl1R2g->Draw(\"APL*\");\n")
  plots.write(arprl2L1)
  plots.write("TGraph* prl2L1g = new TGraph(" + str(len(run)) + ", x, prl2L1);\n")
  plots.write("prl2L1g->SetTitle(\""+arm+" Pion Rejector 2 Left First Half HV sum\");\n")
  plots.write("prl2L1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl2L1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(1);\nprl2L1g->Draw(\"APL*\");\n")
  plots.write(arprl2L2)
  plots.write("TGraph* prl2L2g = new TGraph(" + str(len(run)) + ", x, prl2L2);\n")
  plots.write("prl2L2g->SetTitle(\""+arm+" Pion Rejector 2 Left Second Half HV sum\");\n")
  plots.write("prl2L2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl2L2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(2);\nprl2L2g->Draw(\"APL*\");\n")
  plots.write(arprl2R1)
  plots.write("TGraph* prl2R1g = new TGraph(" + str(len(run)) + ", x, prl2R1);\n")
  plots.write("prl2R1g->SetTitle(\""+arm+" Pion Rejector 2 Right First Half HV sum\");\n")
  plots.write("prl2R1g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl2R1g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(3);\nprl2R1g->Draw(\"APL*\");\n")
  plots.write(arprl2R2)
  plots.write("TGraph* prl2R2g = new TGraph(" + str(len(run)) + ", x, prl2R2);\n")
  plots.write("prl2R2g->SetTitle(\""+arm+" Pion Rejector 2 Right Second Half HV sum\");\n")
  plots.write("prl2R2g->SetMaximum(" + str(1.1) + ");\n")
  plots.write("prl2R2g->SetMinimum(" + str(0.9) + ");\n")
  plots.write("calo2->cd(4);\nprl2R2g->Draw(\"APL*\");\n")
plots.write(arvdc)
plots.write("TGraph* vdcg = new TGraph(" + str(len(run)) + ", x, vdc);\n")
plots.write("vdcg->SetTitle(\""+arm+" VDC HV sum\");\n")
plots.write("vdcg->SetMaximum(" + str(1.1) + ");\n")
plots.write("vdcg->SetMinimum(" + str(0.9) + ");\n")
plots.write("vdcc->cd(0);\nvdcg->Draw(\"APL*\");\n")

try:
  os.remove("hv"+arm+".pdf")
except OSError:
  pass

plots.write("s0gc->Print(\"hv"+arm+".pdf(\",\"pdf\");\n")
plots.write("s2c->Print(\"hv"+arm+".pdf\",\"pdf\");\n")
plots.write("calo1->Print(\"hv"+arm+".pdf\",\"pdf\");\n")
plots.write("calo2->Print(\"hv"+arm+".pdf\",\"pdf\");\n")
plots.write("vdcc->Print(\"hv"+arm+".pdf)\",\"pdf\");\n")

plots.write("gApplication->Terminate();\n")

plots.write("}\n")
plots.close()

root_query = ['root','-l','hv_plots.C']
root = subprocess.Popen(root_query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #run root
root.communicate()
