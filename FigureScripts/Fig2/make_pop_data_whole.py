#-*-encoding:utf-8 -*-

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

	
def FindTypes(fname, ti, tf):
	BD = {}
	prev = []
	fp = open(fname, 'r')
	lines = fp.readlines()
	fp.close()

	#making birth, death time data for types being in time period of ti:tf
	for i in range(ti, tf):
		elem = re.split(" |\t|\n", lines[i])
		n = int(elem[3])
		
		#making a list of types; if there is new type, make a BD dic.
		curr = []
		for k in range(n):
			idx = int(elem[4+n+k])
			curr.append(idx)
			if idx in BD:
				1
			else:
				BD[idx] = [i]
		
		#checking the death of types
		for k in prev:
			if k in curr:
				1
			else: 
				BD[k].append(i)

		#update the list
		prev = curr
		

	#giving a threshold and select relevant types 
	types = []
	th = 2	#thresold: if a type survived more than th, we will pick this type
	for item in BD:
		if len(BD[item])>1:
			if BD[item][1]-BD[item][0]>th:
				types.append(item)
		else:
			if tf-BD[item][0]>th:
				types.append(item)
	
	types = sorted(types)
	idx_types = {}
	for i in range(len(types)):
		idx_types[types[i]] = i

	return len(types), types, idx_types


fidx = int(sys.argv[1])
tmax = 10000
fname = "M1000_mu1e-05_d0.005_maxt%d_%d.d" % (tmax, fidx)


ti = 0
tf = 200
tot_n, sur_types, idx_types = FindTypes(fname, ti, tf)
#print "tot_n=", tot_n, sorted(sur_types)

#main
fp = open(fname, 'r')
lines = fp.readlines()
fp.close()
abundance = np.zeros([tot_n, tf-ti+1])
for l in range(ti, tf):
	elem = re.split(" |\t|\n", lines[l])
	n = int(elem[3])
	for i in range(n):
		species = int(elem[4+n+i])
		if species in sur_types:
			idx = idx_types[species]
			abundance[idx][l-ti] = int(elem[4+i])

#writing
fname = "abundances_%d.d" % fidx
fp = open(fname, 'w')
for t in range(ti, tf):
	fp.write("%d " % t)
	for idx in range(len(sur_types)):
		fp.write("%d " % abundance[idx][t-ti])
	fp.write("\n")
fp.close()

#making plot script
fname_gnu = "gnu.abundances_%d.gpi" % fidx
fp = open(fname_gnu, "w")
fp.write("set t po eps enh color 15\nset output \"abundances_%d.eps\"\nset border lw 2\nset tics scale 1 \n" % fidx)
fp.write("set label\"Abundances\" rotate center at screen 0.02, 0.55 font \",15\"\nset xlab \"Time\" font \",15\"\n")
fp.write("set ytics 1000\nset xtics 20\nset xr[:160]\nset size ratio 0.2\nset style fill solid 0.8 noborder\nload \'gnu.color.gpi\'\n")

#making string
macro = ""
for i in range(tot_n):
	macro += "$%d+" % (2+i) 
macro = macro[:len(macro)-1]


fp.write("p \'%s\' u 1:(%s):(%s) w filledcurves ls 1 t \'\' \\\n" %(fname, macro[3:], macro) )
for i in range(1, tot_n-1):
	if i<9:
		fp.write(",\'%s\' u 1:(%s):(%s) w filledcurves ls %d t \'\'\\\n" %(fname, macro[3*(i+1):], macro[3*(i):], i+1) )
	elif i<99: 
		fp.write(", \'%s\' u 1:(%s):(%s) w filledcurves ls %d t \'\'\\\n" %(fname, macro[32+4*(i-9):], macro[32+4*(i-10):], i+1) )
	else: 
		fp.write(", \'%s\' u 1:(%s):(%s) w filledcurves ls %d t \'\'\\\n" %(fname, macro[394+5*(i-99):], macro[394+5*(i-100):], i+1) )
fp.write(", \'%s\' u 1:($%d) w filledcurves x1 ls %d t \'\'\n" % (fname, tot_n+1, tot_n))
if tot_n>999:
	print 'you need to change the gnuplot code for tot_n>999'
