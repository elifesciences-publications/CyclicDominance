#-*-encoding:utf-8 -*-
################################################################
# 2019-01-18												   #
# output file: time seriese of all average payoffs of all elements, only diagonal, only non-diagonal, survival average payoffs of all elements, only diagonal, only non-diagonal
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
	print fname
	lines = fp.readlines()
	Nl = len(lines)
	fp.close()
	flag = 0
	if Nl > tmax+1:
		Nl = tmax+1
	
	
	#all sampled average
	p1 = np.zeros(rec+1)
	pdia1 = np.zeros(rec+1)
	poffdia1 = np.zeros(rec+1)

	for i in range(t0, Nl-1):
		elem = re.split(" |\t|\n", lines[i])
		avg1 = 0; avg2 = 0; avg3 =0;

		#make payoff matrix
		n = int(elem[3])
		for e1 in range(n):
			for e2 in range(n):
				payoff = float(elem[4+2*n+e1*n+e2]) 
				avg1 += payoff
				if e1==e2:
					avg2 += payoff
				else:
					avg3 += payoff
		if n>0:
			avg1 /= (n*n)
			avg2 /= n
			if n>1:
				avg3 /= (n*n-n)
		p1[i-t0] = avg1;
		pdia1[i-t0] = avg2;
		poffdia1[i-t0] = avg3;
	

	#survival sampled average
	p = np.zeros(rec+1)
	pdia = np.zeros(rec+1)
	poffdia = np.zeros(rec+1)

	if(Nl>tmax):
		flag = 1
		for i in range(t0, Nl):
			elem = re.split(" |\t|\n", lines[i])
			avg1 = 0; avg2 = 0; avg3 =0;
    
			#make payoff matrix
			n = int(elem[3])
			for e1 in range(n):
				for e2 in range(n):
					payoff = float(elem[4+2*n+e1*n+e2]) 
					avg1 += payoff
					if e1==e2:
						avg2 += payoff
					else:
						avg3 += payoff
    
			avg1 /= (n*n)
			avg2 /= n
			if n>1:
				avg3 /= (n*n-n)
			p[i-t0] = avg1;
			pdia[i-t0] = avg2;
			poffdia[i-t0] = avg3;
    

	return [flag, p1, pdia1, poffdia1, p, pdia, poffdia]


""" ------------------------------------ """


""" -------- main ---------- """
dlist = [0.05, 0.025,  0.01, 0.0075, 0.005] 
tmax = 10000
mu = 1e-05
l = 0
dir = "l%g" % l
#rec = 500
rec = tmax
t0 = tmax - rec

for d in dlist:
	flist = CountFile(dir, d)
	Nf = len(flist)
	all_p = np.zeros(rec+1)
	all_pdia = np.zeros(rec+1)
	all_poffdia = np.zeros(rec+1)
	sur_p = np.zeros(rec+1)
	sur_pdia = np.zeros(rec+1)
	sur_poffdia = np.zeros(rec+1)

	#--------- read data and get PDF ------------#
	Nsur=0;
	for fname in flist:
		[flag, p1, pdia1, poffdia1, p, pdia, poffdia] = ReadData(dir + "/" + fname)
		all_p += p1
		all_pdia += pdia1
		all_poffdia += poffdia1
		sur_p += p
		sur_pdia += pdia
		sur_poffdia += poffdia
		Nsur += flag


	#--------- calculate avg and std ------------#
	print Nf, Nsur
	all_p /= Nf; 
	all_pdia /= Nf; 
	all_poffdia /= Nf; 
	sur_p /= Nsur; 
	sur_pdia /= Nsur; 
	sur_poffdia /= Nsur; 

	ofp = open("data/avgp_l%g_mu%g_d%g.txt" % (l, mu, d), 'w')	
	ofp.write("#time Ntotal=%d Nsur=%d all average payoffs of all elements, only diagonal, only non-diagonal, sur sampled payoffs \n" % (Nf, Nsur))
	for i in range(rec):
		ofp.write("%d %g %g %g %g %g %g\n" % (t0+i, all_p[i], all_pdia[i], all_poffdia[i], sur_p[i], sur_pdia[i], sur_poffdia[i]))
	
