#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" computes the number of chi in random matrices with n """
"""
input : n
output: n, chi
descript: random matrix --- all elements from the random variables with white noise
"""

import numpy as np
import analysis_triad as at
import matplotlib.pyplot as plt

def RandomMatricesTriad(n):

	""" sample size """
	N=500000
	
	Result = np.zeros(16)
	for i in np.arange(N):
		Matrix = np.random.normal(0, 1, (n,n))
		CurrentCount = np.zeros(16)
		at.CountTriads(CurrentCount, Matrix, n)
		Result += CurrentCount
	
	Result = Result / (N*n*(n-1)*(n-2)/6)
	
	return Result


""" main code writing to file"""
res = {}
for n in range(3, 20):
	Result = RandomMatricesTriad(n)
	IDs = np.arange(16)
	DataToFile = [IDs, Result]
	np.savetxt("Random/TriadDist_n%d.txt" % (n) , DataToFile, fmt='%.4e')

	chi =  Result[14]/(Result[14]+Result[15])
	print n, chi
	res[n] = chi
	
