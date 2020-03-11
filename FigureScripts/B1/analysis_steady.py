#-*-encoding:utf-8 -*-
################################################################
# 2019-12												   #

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys


dlist = [0.5, 0.1, 0.05, 0.01, 0.005]
tmax = 10000
mu = 1e-05
Res = []

t0=9500
tf=10000
#------ read data and get the dics of triad14 and triad15 ------------#
for d in dlist:
	fname = "l0_mu1e-05_d%g_tmax10000.txt" % d
	fp = open(fname, 'r')
	lines = fp.readlines()
	s = 0;	N = 0
	for l in range(t0, tf+1):
		elem = re.split(" |\t|\n", lines[l])
		N += float(elem[3]); s += float(elem[7])
	N/= (tf+1-t0);s/= (tf+1-t0)
	Res.append([d, N, s])

		
print Res	

ofp = open("l0_mu1e-05_t10000.txt", 'w')
for i in range(len(Res)):
    for j in range(len(Res[i])):
		ofp.write("%g " % Res[i][j])
    ofp.write("\n")