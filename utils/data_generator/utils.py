import scipy.stats as ss
import numpy as np
import itertools
import sys

def get_records_files(expected):
    args = sys.argv
    if len(args) != expected + 1:
        raise Exception(f'{expected} arguments required')

    return tuple([int(arg) for arg in args[1:]])

def get_n_records_iter(it, n):
    return itertools.islice(it, n)

def get_normal_dist(maxim, stdev, samples):
    x = np.arange(0, maxim + 1)
    xU, xL = x + 0.5, x - 0.5 
    prob = ss.norm.cdf(xU, scale = stdev) - ss.norm.cdf(xL, scale = stdev)
    prob = prob / prob.sum()
    nums = np.random.choice(x, size = samples, p = prob)
    return nums
