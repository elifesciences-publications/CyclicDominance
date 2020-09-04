#-*-encoding:utf-8 -*-
""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

dlist = [0.005]
#0.05, 0.025, 0.01,0.0075,0.005
t1 = 9500
t2 = 10000
maxt = 10000

res = []
for d in dlist:
	fp = open('../Res/ts_d%g_mu1e-05_t%d.txt' % (d, maxt+1 ), 'r')
	lines = fp.readlines()
	fp.close()
	t14 = []
	t15 = []
	Dt14 = []
	Dt15 = []
	n = []
	Dn = []

	for i in range(t1, t2):
		elem = re.split(" |\t|\n", lines[i])
		n.append(float(elem[1]))
	   	Dn.append(float(elem[2]))
		t14.append(float(elem[3]))
   		Dt14.append(float(elem[4]))
   	 	t15.append(float(elem[5]))
   	 	Dt15.append(float(elem[6]))

	#--------- recoding  ------------#
	t14 = np.array(t14)
	t15 = np.array(t15)
	Dt14 = np.array(Dt14)
	Dt15 = np.array(Dt15)
	n = np.array(n)
	Dn = np.array(Dn)
	chi = t14/(t14+t15)
	min_chi = (t14-Dt14)/(t14-Dt14+t15+Dt15)
	max_chi = (t14+Dt14)/(t14+Dt14+t15-Dt15)
	res.append([d, np.mean(n), np.mean(Dn), np.mean(t14), np.mean(Dt14), np.mean(t15), np.mean(Dt15),  np.mean(chi), np.mean(min_chi), np.mean(max_chi)])


#---- writing ----#
Nen = t2-t1
ofp = open("../Res/chi_mu1e-05.txt", 'w')	
ofp.write("#d survival averaged n, sdt_n, t14, std_t14, t15, std_t15,  chi, min_chi, max_min\n")
for l in range(len(dlist)):
	for i in range(10):
		ofp.write("%g " % res[l][i] )
	ofp.write("\n")
