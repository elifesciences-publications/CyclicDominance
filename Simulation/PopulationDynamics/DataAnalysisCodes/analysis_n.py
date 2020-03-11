#-*-encoding:utf-8 -*-
################################################################
# 2018-01-10												   #
# output file: p(n)
# output file: wij
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
	
	
	tempn = np.zeros(maxn)
	tempw = np.zeros((maxn, maxn))
	t0 = 8000
	flag = 0
	
	if(Nl>tmax):
		flag = 1
		elem = re.split(" |\t|\n", lines[t0-1])
		ntm1 = int(elem[3])
		for l in range(t0, Nl):
			elem = re.split(" |\t|\n", lines[l])
			nt = int(elem[3])
			tempn[nt] += 1
			tempw[ntm1][nt] += 1
			ntm1 = nt
		tempn /= sum(tempn)
		tempw /= sum(tempn)
	
	
	return [flag, tempn, tempw]


""" ------------------------------------ """


""" -------- main ---------- """
#dlist = [0.5, 0.3, 0.1, 0.05, 0.03, 0.01, 0.005, 0.003, 0.001]
dlist = [ 0.3, 0.03, 0.005]
tmax = 10000
mu = 1e-05
l = 0
dir = "l%g" % l
maxn = 100

for k in range(len(dlist)):
	d = float(dlist[k])
	flist = CountFile(dir, d)
	Nf = len(flist)
	n = np.zeros(maxn)
	w = np.zeros((maxn,maxn))

	#--------- read data and get PDF ------------#
	Nsur=0;
	for fname in flist:
		[flag, tempn, tempw] = ReadData(dir + "/" + fname)
		n += tempn
		w += tempw
		Nsur += flag


	#--------- calculate avg and std ------------#
	n /= Nsur; 
	w /= Nsur; 

	ofpn = open("data/n_l%g_mu%g_d%g.txt" % (l, mu, d), 'w')	
	ofpw = open("data/w_l%g_mu%g_d%g.txt" % (l, mu, d), 'w')	
	ofpn.write("#p(n1) p(n2) ...\n")
	avgn = 0.;
	for i in range(1, maxn):
		ofpn.write("%d %g\n" % (i, n[i]))
		avgn += i*n[i]
		for j in range(1, maxn):
			ofpw.write("%g " % w[i][j])
		ofpw.write("\n")
	
	
	#--------- calculate <n> given mu and d ------------#
	print(mu, d, avgn)
