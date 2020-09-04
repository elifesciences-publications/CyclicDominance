#-*-encoding:utf-8 -*-
################################################################
# 2019-01-18: averaging distributions of links												   #
# output file: average payoffs of all elements fraction of dominance, coordination, coexistence
################################################################

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

def CountFile(dirpath, d):
	name = "M1000_mu%g_d%g_maxt%d_*.d" % (mu, d, tmax) 
	return fnmatch.filter(os.listdir(dirpath), name)


def  MakeFileList(dirpath, d, Nen):
	flist = []
	for i in range(Nen):
		name = "M1000_mu%g_d%g_maxt%d_%d.d" % (mu, d, tmax, i) 
		flist.append(name)

	return flist



def ReadData(fname):
	fp = open(fname, 'r')
	print fname
	lines = fp.readlines()
	Nl = len(lines)
	fp.close()
	if Nl > tmax+1:
		Nl = tmax+1
	
	
	links = np.zeros([rec+1, 3])
	
	for i in range(t0, Nl):
		elem = re.split(" |\t|\n", lines[i])
		avg = 0
		frac = np.zeros(3)

		#make payoff matrix
		n = int(elem[3])
		if n>1:
			matrix = np.zeros([n,n])
			for e1 in range(n):
				for e2 in range(n):
					matrix[e1][e2] = float(elem[4+2*n+e1*n+e2]) 
    
			#find links
			nlinks = (float(n)*(n-1.)/2.)
			for e1 in range(n):
				for e2 in range(e1):
					if matrix[e1][e1] < matrix[e2][e1]:
						if matrix[e2][e2] < matrix[e1][e2]:
							frac[2]+=1
						else:
							frac[0] +=1
					elif matrix[e2][e2] > matrix[e1][e2]:
						frac[1]+=1
					else:
						frac[0]+=1
			frac /= nlinks 
			links[i-t0] = frac
    
	
	flag = 0
	if(Nl>tmax):
		flag = 1

	return [flag, links]


""" ------------------------------------ """


""" -------- main ---------- """
#dlist = [0.01, 0.009, 0.008,  0.007, 0.006, 0.005] 
dlist = [0.005]
tmax = 10000
mu = 1e-05
dir = "../data"
rec = tmax
t0 = tmax - rec
Data = {}
Nen = 100

for d in dlist:
	flist = CountFile(dir, d)
	Nf = len(flist)
	avglinks = np.zeros([rec+1, 3])	
	surlinks = np.zeros([rec+1, 3])	
	all1 = np.zeros(501)
	all2 = np.zeros(501)
	all3 = np.zeros(501)
	sur1 = np.zeros(501)
	sur2 = np.zeros(501)
	sur3 = np.zeros(501)

	#--------- read data and get PDF ------------#
	Nsur=0;
	for fname in flist:
		[flag, links] = ReadData(dir + "/" + fname)
		avglinks += links
		if flag:
			surlinks += links
		Nsur += flag


	#--------- calculate avg and std ------------#
	avglinks /= Nf;
	surlinks /= Nsur;


	ofp = open("../Res/links_mu%g_d%g.txt" % (mu, d), 'w')	
	ofp.write("#t, all sampled fraction of dominance, coordination, coexistence sur_sampled fraction of dominance coordination coexistence\n")
	for i in range(rec):
		ofp.write("%d " % (i))
		for l in range(3):
			ofp.write("%g " % avglinks[i][l])
		for l in range(3):
			ofp.write("%g " % surlinks[i][l])
		ofp.write("\n")

		if i>=9500:
			all1[i-9500] = avglinks[i][0];	all2[i-9500] = avglinks[i][1];	all3[i-9500] = avglinks[i][2];
			sur1[i-9500] = surlinks[i][0];	sur2[i-9500] = surlinks[i][1];	sur3[i-9500] = surlinks[i][2];

	#---- calculate the average at steady state
	Data[d] = np.array([np.mean(all1), np.mean(all2), np.mean(all3), np.mean(sur1), np.mean(sur2), np.mean(sur3)])	

	
	
ofp = open("../Res/links_mu%g_tmax%d.txt" % (mu, tmax), 'w')
ofp.write("#d all averaged fraction of links (dominance, coordination, coexistence) surviving averaged one for three (dominance, coordination, coexistence)\n")
for d in dlist:
	ofp.write("%g %g %g %g %g %g %g\n" % (d, Data[d][0], Data[d][1], Data[d][2], Data[d][3], Data[d][4], Data[d][5]))
