#-*-encoding:utf-8 -*-
################################################################
import re
import os
import numpy as np
import fnmatch
import sys

ti=9500
tf=10000

fname = '../Res/matrix_d0.005_t%d_t%d.txt' % (ti, tf) 
fp = open(fname, 'r')
lines = fp.readlines()
Nl = len(lines)

PDF14 = np.zeros(501)
PDF15 = np.zeros(501)
for l in range(1, Nl):
	elem = re.split("\t| |\n", lines[l])
	lifespan = int(elem[10])-int(elem[9])
	triad = int(elem[11])
	if triad == 14:
		PDF14[lifespan] += 1
	else:
		PDF15[lifespan] += 1



ofp = open("../Res/cdf_t14_t%d_t%d.txt" % (ti, tf), 'w')
ofp.write("#lifespan, pdf, cdf (from 500), lifespan, cdf (from0)\n")
cdf1 = 0
cdf2 = 0
tot = sum(PDF14)
for i in range(0, 501):
	cdf1 += PDF14[500-i] 
	cdf2 += PDF14[i] 
	ofp.write("%d %g %g %d %g\n" % (500-i, PDF14[500-i]/tot, cdf1/tot, i, cdf2/tot))
ofp.close()

ofp = open("../Res/cdf_t15_t%d_t%d.txt" % (ti, tf), 'w')
ofp.write("#lifespan, pdf, cdf (from 500), lifespan, cdf (from0)\n")
cdf1 = 0
cdf2 = 0
tot = sum(PDF14)
for i in range(0, 501):
	cdf1 += PDF15[500-i] 
	cdf2 += PDF15[i] 
	ofp.write("%d %g %g %d %g\n" % (500-i, PDF15[500-i]/tot, cdf1/tot, i, cdf2/tot))
ofp.close()
