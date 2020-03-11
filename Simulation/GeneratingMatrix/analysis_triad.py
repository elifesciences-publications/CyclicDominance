#-*-encoding:utf-8 -*-
################################################################

""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys


def CountTriads(frac, matrix, n):
	#making linktypes
	nl = int(n*(n-1)/2)
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
	
	#calculating the probability to have the same dominance direction
	if n==3:
		if linktypes[n2][n3] == 'a' and linktypes[n1][n3] == 'a': 
			return np.array([1, 0])
		elif linktypes[n2][n3] == 'b' and linktypes[n1][n3] == 'b': 
			return np.array([1, 0])
		elif linktypes[n2][n3] == 'a' and linktypes[n1][n3] == 'b': 
			return np.array([0, 1])
		elif linktypes[n2][n3] == 'b' and linktypes[n1][n3] == 'a': 
			return np.array([0, 1])
		else: 
			return np.array([0, 0])

def col(matrix, i):
	return sum(matrix[i])/len(matrix[i])

def row(matrix, i):
	vec = [ row[i] for row in matrix ]
	return sum(vec)/len(vec)


#making triads dictionary
dic = {}
fp = open('triads.txt', 'r')
lines = fp.readlines()
for i in range(1, len(lines)):
	elem = re.split(' |\t|\n', lines[i])
	if elem[1] in dic:
		print("something wrong in the file triads.txt")
	else:
		dic[elem[1]] = int(elem[0])
