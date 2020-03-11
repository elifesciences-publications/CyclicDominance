#-*-encoding:utf-8 -*-

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

	
#fidx = int(sys.argv[1])
fidx = 129
tmax = 10000
fname = "M1000_mu1e-05_w1_d0.005_maxt%d_%d.d" % (tmax, fidx)
os.system("cat tree_%s | awk '{print $2, $1}' > ../tree%d.d" % (fname, fidx))
fp = open(fname, 'r')
lines = fp.readlines()
fp.close()

#for fidx=104
#tot_n = 13
#sur_types = [0, 5, 13, 17, 62, 65,  68, 78, 79, 155, 177, 197, 199] #, 200]

#for fidx=129
tot_n = 11
sur_types = [0, 12, 18, 34, 48, 55,  67, 68, 87, 106, 111]
idx_types = {}
for i in range(len(sur_types)):
	idx_types[sur_types[i]] = i

	
tf = 120
abundance = np.zeros([tot_n, tf])
for l in range(tf):
	elem = re.split(" |\t|\n", lines[l])
	n = int(elem[3])
	for i in range(n):
		species = int(elem[4+n+i])
		if species in sur_types:
			idx = idx_types[species]
			abundance[idx][l] = int(elem[4+i])

fname = "res/abundances_%d.d" % fidx
fp = open(fname, 'w')
for t in range(tf):
	fp.write("%d " % t)
	for idx in range(len(sur_types)):
		fp.write("%d " % abundance[idx][t])
	fp.write("\n")


#making plot script
fname = "gnu.abundances_%d.gpi" % fidx
fp = open(fname, "w")
fp.write("set t po eps enh color 15\nset output \"abundances_%d.eps\"\nset border lw 2\nset tics scale 1 \n" % fidx)
fp.write("set label\"Abundances\" rotate center at screen 0.02, 0.55 font \",15\"\nset xlab \"Time\" font \",15\"\n")
fp.write("set ytics 10000\nset xtics 20\nset xr[:%d]\nset size ratio 0.2\nset style fill solid 0.8 noborder\nload \'gnu.color.gpi\'\n" % tf)
Ntype = 10
#color = [2 ,3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]
color = [2 ,3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]

#making string
macro = ""
for i in range(Ntype):
	macro += "$%d+" % (2+i) 
macro = macro[:len(macro)-1]

fp.write("p \'res/abundances_129.d\' u 1:(%s):(%s) w filledcurves ls %d t \'\' \\\n" %(macro[3:], macro, color[i]) )
for i in range(1, Ntype-1):
	fp.write(", \'res/abundances_129.d\' u 1:(%s):(%s) w filledcurves ls %d t \'\'\\\n" %(macro[3*(i+1):], macro[3*(i):], color[i-1]) )
fp.write(", \'res/abundances_129.d\' u 1:($11) w filledcurves x1 ls 12llll t \'\'\n")
