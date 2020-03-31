#-*-encoding:utf-8 -*-
################################################################
# 2019-12												   #

import re
import os
import numpy as np
import fnmatch
import sys


def Stat(m):
	#making trait vectors
	e1 = 0; e2=1; e3 = 2;
	v1 = np.array([m[e1][e1], m[e1][e2], m[e1][e3], m[e1][e1], m[e2][e1], m[e3][e1]])
	v2 = np.array([m[e2][e1], m[e2][e2], m[e2][e3], m[e1][e2], m[e2][e2], m[e3][e2]])
	v3 = np.array([m[e3][e1], m[e3][e2], m[e3][e3], m[e1][e3], m[e2][e3], m[e3][e3]])

	#extracting mean vector
	avg = sum(v1+v2+v3)/18.
	v1 -=avg
	v2 -=avg
	v3 -=avg

	cos_sim = np.zeros(3)
	cos_sim[0] = sum(v1*v2)
	cos_sim[1] = sum(v2*v3)
	cos_sim[2] = sum(v3*v1)
	mean = np.mean(cos_sim)
	std = np.std(cos_sim)
	
	return [mean, std]


#open the raw data file
fname = "../Res/matrix_d0.005_t9500_t10000.txt"
fp = open(fname, 'r')
lines = fp.readlines()
Nl = len(lines)

#calculating
m = np.zeros([3,3])	
t14 = []
t15 = []
for l in range(1, Nl):
	elem = re.split(" |\t|\n", lines[l])
	#matrix
	for i in range(3):
		for k in range(3):
			m[i][k] = float(elem[i*3+k])
	triplet = int(elem[11])

	#get stat
	arr = Stat(m)
	print arr, type(arr)
	if triplet == 14:
		t14.append(arr)
	else:
		t15.append(arr)

#writing
fname = "../Res/t14_scatter.txt"
ofp = open(fname, "w")
for arr in t14:
	ofp.write("%g %g\n" % (arr[0], arr[1]))

fname = "../Res/t15_scatter.txt"
ofp = open(fname, "w")
for arr in t15:
	ofp.write("%g %g\n" % (arr[0], arr[1]))
