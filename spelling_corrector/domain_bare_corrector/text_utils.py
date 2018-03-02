# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import editdistance
import os
import utils
import math

cdir = os.path.abspath(os.path.dirname(__file__))

ENDING_MARKER = re.compile(ur"[\,\.\;\?\!]*$",re.UNICODE)
DIGIT = re.compile(ur"\d")
REMOVE_CHAR = re.compile(ur"[\"\(\)\?\:\“]",re.UNICODE)
MISS_SPACE = re.compile(ur"(?P<BF>\w)(?P<GG>,)(?P<AT>\w)",re.UNICODE)
DMIN = 5

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

def split_dot(token):
    res = []
    if DIGIT.search(token) == None:
        parts = token.split(".")
        for p in parts:
            if len(p)> 0:
                res.append(p)
    else:
        res.append(token)
    return res

def split_sentece(sen):
    tokens = sen.split(" ")
    res = []
    for token in tokens:
        ss = split_dot(token)
        for s in ss:
            res.append(s)
    return res
def is_skip_token(token):
    if len(token)<2:
        return True
    for c in token:
        if c.isdigit():
            return True
    if token.__contains__(",") or token.__contains__(".."):
        return True
    return False
def norm_token(token):
    token2 = unicodedata.normalize('NFC',token)
    token2 = REMOVE_CHAR.sub("", token2)
    token2 = MISS_SPACE.sub(ur"\g<BF>\g<GG> \g<AT>",token2)
    return ENDING_MARKER.sub("",token2)




def accent2bare(data):
    data = data.lower()
    s = ""
    for c in data.lower():
        try:
            s += conv_dict[c]
        except:
            s += c
    return s