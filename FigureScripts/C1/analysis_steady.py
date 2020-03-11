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
	fname = "./links_l0_mu1e-05_d%g.txt" % d
	fp = open(fname, 'r')
	lines = fp.readlines()
	l1 = 0;	l2 = 0; l3=0
	for l in range(t0, tf+1):
		elem = re.split(" |\t|\n", lines[l])
		l1 += float(elem[4]); l2 += float(elem[5]); l3 += float(elem[6])
		sum = l1+l2+l3
	l1/= (tf+1-t0);l2/= (tf+1-t0);l3/= (tf+1-t0)
	sum = l1+l2+l3
	Res.append([d, l1/sum, l2/sum, l3/sum])

		
print Res	
