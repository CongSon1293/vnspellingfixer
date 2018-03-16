# -*- coding: utf-8 -*-

import cPickle as pickle

import re
import sys
from io import open
import numpy


#END_MARKER_RE = re.compile(ur"(?<=\w)(?P<MARKER>[\,\.\;\?\:\!\”\"\)])(?=\s|$)", re.UNICODE)
#START_MARKER_RE = re.compile(ur"(?<!\S)(?P<MARKER>[\(\“])(?=\w)",re.UNICODE)
END_MARKER_RE = re.compile(ur"(?P<MARKER>[\,\.\;\?\:\!\”\"\)])", re.UNICODE)
START_MARKER_RE = re.compile(ur"(?P<MARKER>[\(\“])",re.UNICODE)

conv_dict = {u'a':u'a', u'á':u'a', u'à':u'a', u'ạ':u'a', u'ã':u'a', u'ả':u'a',
			u'ă':u'a', u'ắ':u'a', u'ằ':u'a', u'ặ':u'a', u'ẵ':u'a', u'ẳ':u'a',
			u'â':u'a', u'ấ':u'a', u'ầ':u'a', u'ậ':u'a', u'ẫ':u'a', u'ẩ':u'a',
			u'e':u'e', u'é':u'e', u'è':u'e', u'ẹ':u'e', u'ẽ':u'e', u'ẻ':u'e',
			u'ê':u'e', u'ế':u'e', u'ề':u'e', u'ệ':u'e', u'ễ':u'e', u'ể':u'e',
			u'i':u'i', u'í':u'i', u'ì':u'i', u'ị':u'i', u'ĩ':u'i', u'ỉ':u'i',
			u'o':u'o', u'ó':u'o', u'ò':u'o', u'ọ':u'o', u'õ':u'o', u'ỏ':u'o',
			u'ô':u'o', u'ố':u'o', u'ồ':u'o', u'ộ':u'o', u'ỗ':u'o', u'ổ':u'o',
			u'ơ':u'o', u'ớ':u'o', u'ờ':u'o', u'ợ':u'o', u'ỡ':u'o', u'ở':u'o',
			u'u':u'u', u'ú':u'u', u'ù':u'u', u'ụ':u'u', u'ũ':u'u', u'ủ':u'u',
			u'ư':u'u', u'ứ':u'u', u'ừ':u'u', u'ự':u'u', u'ữ':u'u', u'ử':u'u',
			u'y':u'y', u'ý':u'y', u'ỳ':u'y', u'ỵ':u'y', u'ỹ':u'y', u'ỷ':u'y',
			u'd':u'd', u'đ':u'd'}

def accent2bare(data):
    data = data.lower()
    s = ""
    for c in data.lower():
        try:
            s += conv_dict[c]
        except:
            s += c
    return s

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
def get_update_dict(d,k,v=0):
    try:
        v = d[k]
    except:
        d[k] = v
    return v
def get_abbv_bigram(bigram):
    pairs  = bigram.split(" ")
    if len(pairs) >= 2:
        abb = "%s%s" % (pairs[0][0], pairs[1][0])
    else:
        abb = pairs[0][0]
    return abb
def get_abbv_chars(bigram):
    pairs = bigram.split(" ")
    if len(pairs) >= 2:
        a,b = pairs[0][0],pairs[1][0]
    else:
        a,b = pairs[0][0],""
    return a,b

def generate_hierachical_abbv_dict(ddict):
    abbv_dict = {}
    for k,v in ddict.iteritems():
        abb  = get_abbv_bigram(k)
        try:
            d = abbv_dict[abb]
        except:
            d = {}
            abbv_dict[abb] = d
        d[k] = v
    return abbv_dict

def generate_hierachical_abb_two_level_dict(ddict):
    abbv_dict = {}
    for k,v in ddict.iteritems():
        a,b  = get_abbv_chars(k)
        sub_a = get_update_dict(abbv_dict,a,{})
        sub_b = get_update_dict(sub_a,b,{})
        sub_b[k] = v
    return abbv_dict

def get_abb_two_level_dict(ddict,a,b):
    sub_a = get_zero_dict(ddict,a)
    if sub_a == 0:
        return 0
    sub_b = get_zero_dict(sub_a,b)
    return sub_b


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
def norm_space_marker(sen):
    sen = END_MARKER_RE.sub(" \g<MARKER>",sen)
    sen = START_MARKER_RE.sub("\g<MARKER> ",sen)
    return sen

if __name__ == "__main__":
    s= accent2bare( u"mọt")
    #s2 = accent2bare(u"đk")
    #print lcs(s,s2)
    #END_MARKER_RE = re.compile(ur"(?<=\w)(?P<MARKER>[\,\.\;\?\:\!\”\"\)])(?=\s|$)", re.UNICODE)

    s = u"de toi! xem no (the nao) da. Dung khong?"
    #s = END_MARKER_RE.sub(" \g<MARKER>",s)
    print norm_space_marker(s)
    print s