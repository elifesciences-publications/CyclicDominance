#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output: sigma, chi, triad14, triad15, P(the same dominance direction with its parent), P(the opposite dominance direction)
description: matrix --- type 1 and type 2 are sampled from Gaussian with sigma=1
and then third type originated from 2 with sigma (control parameter)
"""

import numpy as np
import analysis_triad as at
import matplotlib.pyplot as plt
import sys

def MakeMatrix(sigma):
	Matrix = np.zeros([3,3])

	#make 2 by 2 matrix (type one and type 2)
	Matrix[0][0] = np.random.normal(0, 1)
	a = Matrix[0][0];
	Matrix[0][1] = np.random.normal(a, 1) 
	Matrix[1][0] = np.random.normal(a, 1) 
	Matrix[1][1] = np.random.normal(a, 1) 


	#sampling payoff for emerging type 3 with sigma
	idx = 2 
	mom = 1
	for k in range(2):
		Matrix[k][idx] = Matrix[k][mom] + np.random.normal(0, sigma)
		Matrix[idx][k] = Matrix[mom][k] + np.random.normal(0, sigma)
	Matrix[idx][idx] = Matrix[mom][mom] + np.random.normal(0, sigma)

	return Matrix


""" sample size """
#N=500000
N=50
n = 3
res = {}
list_sigma = {0.01, 0.025, 0.05, 0.075,  0.1, 0.25, 0.5, 0.75,  1, 2.5, 5, 7.5, 10, 25, 50, 75, 100}

for sigma in list_sigma:
	result = np.zeros(16)
	prob = np.zeros(2)
	for i in range(N):
		Matrix = MakeMatrix(sigma)
		dist = np.zeros(16)
		prob += at.CountTriads(dist, Matrix, n)
		result += dist

	result /= N
	prob /= N

	chi = result[14]/(result[14]+result[15])
	res[sigma] = [chi, result[14], result[15], prob[0], prob[1]]	

print res
