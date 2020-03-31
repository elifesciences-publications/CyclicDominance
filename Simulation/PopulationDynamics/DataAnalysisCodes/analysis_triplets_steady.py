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


def Link(matrix, e1, e2):
	letter = 'c'
	if matrix[e1][e1] < matrix[e2][e1]:
		if matrix[e2][e2] > matrix[e1][e2]:
			letter = 'b'
	elif matrix[e2][e2] < matrix[e1][e2]:
		letter = 'a'

	return letter


def ReadData(fname):
	fp = open(fname, 'r')
	#print fname
	lines = fp.readlines()
	Nl = len(lines)
	fp.close()
	if Nl > tmax:
		Nl = tmax

	prev = {} #dic of previous triads
	if(Nl>=tmax):
		for i in range(9500, 10000):
			elem = re.split(" |\t|\n", lines[i])
			n = int(elem[3])
			
			curr = {}
			if n>2:
				#making name list and payoff matrix	
				names = np.zeros(n)
				for e1 in range(n):
					names[e1] = int(elem[4+n+e1])
				matrix = np.zeros([n,n])
				for e1 in range(n):
					for e2 in range(n):
						matrix[e1][e2] = float(elem[4+2*n+e1*n+e2]) 
	
				
				#making dic of current traids: key:names with types, value: triad type
				for e1 in range(n):
					for e2 in range(e1):
						for e3 in range(e2):
							arr = np.sort([names[e1], names[e2], names[e3]])
							key = str(arr[0])+ '_' +str(arr[1]) +'_' + str(arr[2])
							if key in prev: 
								curr[key] = prev[key]
							else:
							 	#find the type of triad 
								idx = 'ccc'
								l1 = Link(matrix, e1, e2)
							 	if(l1=='c'):
									idx = 'ccc'
								elif(Link(matrix, e2, e3)=='c'):
									idx = 'ccc'
								else:
									idx = l1
									idx += Link(matrix, e2, e3)
									idx += Link(matrix, e3, e1)
								curr[key] = dic[idx]
								
								#update dic
								if dic[idx] == 14:
									dic14[key] = [matrix[e1][e1], matrix[e1][e2], matrix[e1][e3], matrix[e2][e1], matrix[e2][e2], matrix[e2][e3], matrix[e3][e1], matrix[e3][e2], matrix[e3][e3],  i]
								elif dic[idx] == 15:
									dic15[key] = [matrix[e1][e1], matrix[e1][e2], matrix[e1][e3], matrix[e2][e1], matrix[e2][e2], matrix[e2][e3], matrix[e3][e1], matrix[e3][e2], matrix[e3][e3],  i]

			
			#check which one is destroyed
			for item in prev:
				if item in curr:
					1
				elif prev[item] == 14:
					dic14[item].append(i)
				elif prev[item] == 15:
					dic15[item].append(i)

			#update prev
			prev = curr	
						
							 	


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
dir = "../Data/"
res14 = []
res15 = []

#all averaged samples
flist = CountFile(dir, d)

#------ read data and get the dics of triad14 and triad15 ------------#
for fname in flist:
	dic14 = {}
	dic15 = {}
	print fname
	ReadData(dir + "/" + fname)
	for key in dic14:
		if len(dic14[key])<11:
			dic14[key].append(10000)
		res14.append(dic14[key])
	for key in dic15:
		if len(dic15[key])<11:
			dic15[key].append(10000)
		res15.append(dic15[key])


#-- write --#
ofp = open("../Res/matrix_d%g_t%d_t%d.txt" % (d, 9500, 10000), 'w')
ofp.write("#matrix, time_to_birth, time_to_death\n")
for l in range(len(res14)):
	for i in range(11):
		ofp.write("%g " % (res14[l][i]))
	ofp.write("14\n")

for l in range(len(res15)):
	for i in range(11):
		ofp.write("%g " % (res15[l][i]))
	ofp.write("15\n")
