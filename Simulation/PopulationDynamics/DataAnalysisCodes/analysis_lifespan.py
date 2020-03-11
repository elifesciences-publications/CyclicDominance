#-*-encoding:utf-8 -*-
################################################################
# 2019-01-18: averaging distributions of links												   #
# output file: average payoffs of all elements fraction of dominance, coordination, coexistence
################################################################
def FindLowerSigma(mean, sigma, PDF):
    idx = int(mean)+1
    lower = float(int(mean))
    p = PDF[idx]*(mean+1-idx)
    dx = 0.1

    while p<sigma:
        lower = lower - dx
        idx = int(lower) +1
        p += PDF[idx]*dx
        #print (lower, idx, p, PDF[idx])

    return lower

def FindUpperSigma(mean, sigma, PDF):
    idx = int(mean)+1
    upper = float(int(mean))
    p = PDF[idx]*(mean-idx)
    dx = 0.1

    while p<sigma:
        upper = upper + dx
        idx = int(upper) +1
        p += PDF[idx]*dx
        #print (upper, idx, p, PDF[idx])
        if idx ==500:
            break;

    return upper


""" ------------- functions ----------- """
import re
import os
import numpy as np
import fnmatch
import sys

triad = 15
ti=9500
tf=10000

values = []
fname = 'data/t%d_d0.005_mu1e-05_t%d_t%d.txt' % (triad, ti, tf) 
fp = open(fname, 'r')
lines = fp.readlines()
Nl = len(lines)

LS = []
PDF = np.zeros(501)
for l in range(1, Nl):
	elem = re.split("\t| |\n", lines[l])
	lifespan = int(elem[5])-int(elem[4])
	values.append(lifespan)
	PDF[lifespan] += 1

	
ofp = open("data/cdf_t%d_t%d_t%d.txt" % (triad, ti, tf), 'w')
ofp.write("#lifespan, pdf, cdf (from 500), lifespan, cdf (from0)\n")
cdf1 = 0
cdf2 = 0
tot = sum(PDF)
for i in range(0, 501):
	cdf1 += PDF[500-i] 
	cdf2 += PDF[i] 
	ofp.write("%d %g %g %d %g\n" % (500-i, PDF[500-i]/tot, cdf1/tot, i, cdf2/tot))




#find mean and std, 1sigma
PDF = PDF/tot
values = np.array(values)
median = np.median(values)
mean = np.mean(values)
std = np.std(values)
one_sigma = 0.341

lower = FindLowerSigma(median, one_sigma, PDF)
upper = FindUpperSigma(median, one_sigma, PDF)
tot = 0
std_low = 0
for i in range(0, int(mean)):
    std_low += PDF[i]*(i-mean)*(i-mean)
    tot += PDF[i] 
std_low = np.sqrt(std_low)
tot = 0
std_high = 0
for i in range(int(mean)+1, 501):
    std_high += PDF[i]*(i-mean)*(i-mean)
    tot += PDF[i] 
std_high = np.sqrt(std_high)

print (triad, ti, tf, median, lower, upper, mean, std, std_low, std_high)
