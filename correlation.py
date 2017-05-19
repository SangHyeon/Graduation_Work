from __future__ import print_function
import tensorflow as tf
import numpy as np
import matplotlib
import os
import sys

tf.set_random_seed(777)  # reproducibility

if "DISPLAY" not in os.environ:
    matplotlib.use('Agg')

def PearsonCorrelation(x,y):
    n=len(x)
    vals=range(n)

    #summaition
    sumx = sum([float(x[i]) for i in vals])
    sumy = sum([float(y[i]) for i in vals])

    #square summation
    sumxSq = sum([x[i]**2.0 for i in vals])
    sumySq = sum([y[i]**2.0 for i in vals])\

    #product summation
    pSum = sum([x[i]*y[i] for i in vals])

    #calculate Pearson score
    num = pSum - (sumx*sumy/n)
    den = ((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
    if den==0: return 0

    r = num/den

    return r

data_dim = 2
xy = np.loadtxt('currency_log2.txt', delimiter=',')
var01 = xy[:,[0]]
var02 = xy[:,[1]]
print("=====")
print(var01)
print("-----")
print(var02)

print("*****")

for i in range(data_dim):
    for j in range(data_dim):
        corr = PearsonCorrelation(xy[:,[i]], xy[:,[j]])
        print("{}".format(corr), end=' ')
    print("\n")
