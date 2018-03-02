# -*- coding: utf-8 -*-

import cPickle as pickle
from io import open

import numpy
import re
DIGIT = re.compile(ur"\d")


def lcs2(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[-1][-1]

def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result
def fitler_dict_couter(d,dmin):
    d2 = {}
    for k,v in d.iteritems():
        if v >= dmin:
            d2[k] = v
    del d
    return d2

def filter_dict_digitkey(d):
    d2 = {}
    for k,v in d.iteritems():
        if DIGIT.search(k) == None:
            d2[k] = v
    return d2

def pickle_save(object, path):
    pickle.dump(object, open("%s" % (path), "wb"))
def pickle_load(path):
    return pickle.load(open("%s" % path, "rb"))

def sort_dict(dd):
    kvs = []
    for key, value in sorted(dd.iteritems(), key=lambda (k, v): (v, k)):
        kvs.append([key, value])
    return kvs[::-1]
def sort_dict_idx(dd,idx=2):
    kvs = []
    for key, value in sorted(dd.iteritems(), key=lambda (k, v): (v[idx], k)):
        kvs.append([key, value])
    return kvs[::-1]


def sort_array_indices(ar):
    sorted_args = numpy.argsort(ar)[::-1]
    ar2 = []
    for ind in sorted_args:
        ar2.append(ar[ind])
    return ar2,sorted_args
def add_dict_counter(d,e,v=1):
    try:
        d[e] += v
    except:
        d[e] = v
def get_zero_dict(d,k):
    try:
        v = d[k]
    except:
        v = 0
    return v
def get_dict_element(d,k):
    try:
        v = d[k]
    except:
        v = k
    return v

def generate_hierachical_first_alphabet_dict(ddict):
    hierachical_f_dict = {}
    for k, v in ddict.iteritems():
            c = k[0]
            try:
                d = hierachical_f_dict[c]
            except:
                d = {}
                hierachical_f_dict[c] = d
            d[k] = v
    return hierachical_f_dict
def merge_counting_dict(d1,d2):
    d3 = {}
    for k,v in d1.iteritems():
        d3[k] = v
    for k,v in d2.iteritems():
        try:
            vv = d3[k]
        except:
            vv = 0
        d3[k] = vv + v
    return d3
if __name__ == "__main__":
    pass