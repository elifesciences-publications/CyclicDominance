#-*-encoding:utf-8 -*-
################################################################
# 2019-01-18												   #
# output file: histogram of triads and expectation value from random connection
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


def CountTriads(frac, matrix, n):
	#making linktypes
	nl = n*(n-1)/2
	linktypes = [[0 for temp1 in range(nl)] for temp2 in range(nl)]
	for n1 in range(n):
		for n2 in range(n1):
			if matrix[n1][n1] < matrix[n2][n1]:
				if matrix[n2][n2] < matrix[n1][n2]:
					linktypes[n1][n2] = 'd'
					linktypes[n2][n1] = 'd'
				else:
					linktypes[n1][n2] = 'b'
					linktypes[n2][n1] = 'a'
			elif matrix[n2][n2] > matrix[n1][n2]:
				linktypes[n1][n2] = 'c'
				linktypes[n2][n1] = 'c'
			else:
				linktypes[n1][n2] = 'a'
				linktypes[n2][n1] = 'b'

	#counting triads
	for n1 in range(n):
		for n2 in range(n1):
			for n3 in range(n2):
				idx = linktypes[n1][n2] + linktypes[n2][n3] + linktypes[n3][n1] 
				frac[dic[idx]] += 1
					


def ReadData(fname):
	fp = open(fname, 'r')
	#print fname
	lines = fp.readlines()
	Nl = len(lines)
	fp.close()
	if Nl > tmax+1:
		Nl = tmax+1
	
	
	triad = np.zeros([rec+1, 16])
	flag = 0
	
	if(Nl>tmax):
		flag = 1
		for i in range(t0, Nl):
			elem = re.split(" |\t|\n", lines[i])
			frac = np.zeros(16)

			n = int(elem[3])
			if n>2:
				#make payoff matrix
				matrix = np.zeros([n,n])
				for e1 in range(n):
					for e2 in range(n):
						#print(elem, 4+2*n+e1*n+e2, elem[4+2*n+e1*n+e2])
						matrix[e1][e2] = float(elem[4+2*n+e1*n+e2]) 
	
				#find triads	
				CountTriads(frac, matrix, n)
				ntriads = n*(n-1)*(n-2)/3/2
				frac /= ntriads 
			triad[i-t0] = frac

	return [flag, triad]


	
""" ------------------------------------ """


#making triads dictionary
dic = {}
fp = open('triads.txt', 'r')
lines = fp.readlines()
for i in range(1, len(lines)):
	elem = re.split(' |\t|\n', lines[i])
	if elem[1] in dic:
		print("something wrong in the fiem triads.txt")
	else:
		dic[elem[1]] = int(elem[0])


""" -------- main ---------- """
#calculation
#dlist = [0.5, 0.3, 0.1, 0.05, 0.03, 0.01, 0.005]
dlist = [0.005]
tmax = 10000
mu = 1e-05
dir = "../Data" 
rec = 500
t0 = tmax - rec

for k in range(len(dlist)):
	d = float(dlist[k])
	flist = CountFile(dir, d)
	Nf = len(flist)
	hist = np.zeros([rec+1, 16])


	#--------- read data and get PDF ------------#
	Nsur=0;
	for fname in flist:
		[flag, triad] = ReadData(dir + "/" + fname)
		hist += triad
		Nsur += flag


	#--------- calculate avg and std ------------#
	hist /= Nsur; 
	avg = np.zeros(16)
	div = rec+1
	for i in range(rec+1):
		tot = sum(hist[i])
		if abs(tot)<1e-08:
			tot = 1
			div -= 1
		avg += (hist[i]/tot)
	avg /= div


	#--------- write ------------#
	ofp = open("../Res/triad_mu%g_d%g.txt" % (mu, d), 'w')	
	ofp.write("#triad_ID, fraction\n")
	for i in range(16):
		ofp.write("%d %g\n" % (i, avg[i]) )
