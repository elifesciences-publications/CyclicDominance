#-*-encoding:utf-8 -*-
################################################################
# 2019-12												   #

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

def CountFile(dirpath, d):
	name = "M1000_mu%g_d%g_maxt%d_*.d" % (mu, d, tmax-1) 
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
	if Nl > tmax:
		Nl = tmax
	
	
	flag = 0
	
	nt = np.zeros(tmax)
	p14 = np.zeros(tmax)
	p15 = np.zeros(tmax)

	if(Nl>=tmax):
		flag = 1

		for i in range(Nl):
			elem = re.split(" |\t|\n", lines[i])
			n = int(elem[3])
			nt[i] = n
			
			if n>2:
				#make payoff matrix
				matrix = np.zeros([n,n])
				for e1 in range(n):
					for e2 in range(n):
						#print(elem, 4+2*n+e1*n+e2, elem[4+2*n+e1*n+e2])
						matrix[e1][e2] = float(elem[4+2*n+e1*n+e2]) 
	
				#find triads	
				frac = np.zeros(16)
				CountTriads(frac, matrix, n)
				ntriads = n*(n-1)*(n-2)/3/2
				frac /= ntriads 
				p14[i] = frac[14]
				p15[i] = frac[15]

	return [flag, nt, p14, p15]

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
d = 0.005
tmax = 10000+1
mu = 1e-05
l = 0
dir = "../Data"

#all averaged samples`
res = np.zeros([5, tmax])#ensemble averaged time serise of quantity
samples = np.zeros(tmax)
flist = CountFile(dir, d)
Nf = len(flist)


#--------- read data and get PDF ------------#
Nsur=0;
for fname in flist:
	print fname
	[flag, nt, p14, p15] = ReadData(dir + "/" + fname)
	res[0] += nt #save the time serise of n(t)
	res[1] += p14  #save the time series of probability to find cyclic triad
	res[2] += p14*p14  
	res[3] += p15  
	res[4] += p15*p15
	if flag:
		samples[np.where(nt<3)] += 1
	Nsur += flag
	
samples = Nsur - samples
samples[np.where(samples==0)] = 1
res[0] /= Nsur
res[1] /= samples
res[2] /= samples
res[3] /= samples
res[4] /= samples

res[2] -= res[1]*res[1]
res[2] = np.sqrt(res[2]/samples)
res[4] -= res[3]*res[3]
res[4] = np.sqrt(res[4]/samples)
print Nsur, samples


#--------- write ------------#
ofp = open("../Res/ts_d%g_mu%g_t%d.txt" % (d, mu, tmax), 'w')	
ofp.write("#t, survival_ensemble averaged n, p14, Delta p14, p15, Delta p15, chi\n" )
for t in range(tmax):
	chi = 0
	if res[1][t]+res[3][t] >0:
		chi = res[1][t]/(res[1][t]+res[3][t])
	ofp.write("%d %g %g %g %g %g %g %d\n" % (t, res[0][t], res[1][t], res[2][t], res[3][t], res[4][t], chi, samples[t] ) )
