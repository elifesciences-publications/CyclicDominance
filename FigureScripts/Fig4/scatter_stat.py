#-*-encoding:utf-8 -*-
################################################################


""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

ti=9500
tf=10000


#t14
fname = 't14_scatter.txt'
fp = open(fname, 'r')
lines = fp.readlines()
mc14 = []
Dc14 = []
for l in lines:
	elem = re.split("\t| |\n", l)
	mc14.append(float(elem[0]))
	Dc14.append(float(elem[1]))
mc14 = np.array(mc14)
Dc14 = np.array(Dc14)
print  14, np.mean(mc14), np.std(mc14), np.mean(Dc14), np.std(Dc14)

#t15
fname = 't15_scatter.txt'
fp = open(fname, 'r')
lines = fp.readlines()
mc15 = []
Dc15 = []
for l in lines:
	elem = re.split("\t| |\n", l)
	mc15.append(float(elem[0]))
	Dc15.append(float(elem[1]))
mc15 = np.array(mc15)
Dc15 = np.array(Dc15)
print  15, np.mean(mc15), np.std(mc15), np.mean(Dc15), np.std(Dc15)


