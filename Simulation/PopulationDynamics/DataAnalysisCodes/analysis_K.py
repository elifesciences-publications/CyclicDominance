#-*-encoding:utf-8 -*-
################################################################
# 2018-01-10												   #
# output file: t avgK stdK avgKsur stdKsur avgn stdn avgnsur stdnsur
################################################################

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

def CountFile(dirpath, d):
	name = "M1000_mu%g_w1_d%g_maxt%d_*.d" % (mu, d, tmax) 
	return fnmatch.filter(os.listdir(dirpath), name)



def ReadData(fname):
	fp = open(fname, 'r')
	lines = fp.readlines()
	Nl = len(lines)
	fp.close()
	if Nl > tmax+1:
		Nl = tmax+1

	kt = np.zeros(tmax+1)
	nt = np.zeros(tmax+1)
	for l in range(Nl):
		elem = re.split(" |\t|\n", lines[l])
		kt[l] = int(elem[2])
		nt[l] = int(elem[3])

	flag = 0
	if Nl < tmax+1: #if it goes to extinction
		flag = 1

	return [flag, kt, nt]

def column(matrix, i):
	return [row[i] for row in matrix]

def sum_partial(vector, begin, end):
	tot = 0.
	print len(vector)
	for i in range(begin, end):
		tot += vector[i]

	return tot/(end-begin)
""" ------------------------------------ """


""" -------- main ---------- """
mu = 1e-05
#tmax = 10000
#dlist = [0.05, 0.025,  0.01, 0.0075, 0.005] 
tmax = 20000
dlist = [0.005] 
l=0
dir = "l%g" % l
Data = {}

#get the average values in time at a given d and mu value
for d in dlist:
	#--------- read data and get PDF ------------#
	flist = CountFile(dir, d)
	Nf = len(flist)
	K = np.zeros((4, tmax+1))
	n = np.zeros((4, tmax+1))
	Nsur=0;

	for fname in flist:
		#print fname
		[flag, tempK, tempn] = ReadData(dir + "/" + fname)
		K[0] += tempK
		n[0] += tempn
		K[1] += tempK*tempK
		n[1] += tempn*tempn
		if flag==0:
			K[2] += tempK
			K[3] += tempK*tempK
			n[2] += tempn
			n[3] += tempn*tempn
			Nsur += 1


	#--------- calculate avg and std ------------#
	K[0] /= Nf; K[1] /= Nf; 
	Kg[1] -= K[0]*K[0]
	K[1] = np.sqrt(K[1]/Nf)
	n[0] /= Nf; n[1] /= Nf; 
	n[1] -= n[0]*n[0]
	n[1] = np.sqrt(n[1]/Nf)

	K[2] /= Nsur; K[3] /= Nsur;
	K[3] -= K[2]*K[2]
	K[3] = np.sqrt(K[3]/Nsur)
	n[2] /= Nsur; n[3] /= Nsur;
	n[3] -= n[2]*n[2]
	n[3] = np.sqrt(n[3]/Nsur)

	#--------- write ---------------#
	ofp = open("data/l%g_mu%g_d%g_tmax%d.txt" % (l, mu, d, tmax), 'w')	
	ofp.write("#t with Nf=%d Nsur=%d K_all std K_sur std n_all std n_sur std\n" % (Nf, Nsur))
	for i in range(tmax+1):
		ofp.write("%d " % i )
		for j in range(4):
			ofp.write("%g " % K[j][i])
		for j in range(4):
			ofp.write("%g " % n[j][i])
		ofp.write("\n")
	
	Data[d] = np.array([sum_partial(K[0], 9500, 10000), sum_partial(K[2], 9500, 10000), sum_partial(n[0], 9500, 10000), sum_partial(n[2], 9500, 10000)])
	print Data

	
	
	
ofp = open("data/nN_mu%g_tmax%d.txt" % (mu, tmax), 'w')
ofp.write("#d avgK surK avgn surn\n")
for d in dlist:
	ofp.write("%g %g %g %g %g\n" % (d, Data[d][0], Data[d][1], Data[d][2], Data[d][3]))
