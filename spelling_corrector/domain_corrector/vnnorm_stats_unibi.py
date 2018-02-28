# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open

import spelling_corrector.domain_corrector.text_utils
import utils
#from custom_regex import HardRegex,CommonRegex
import math
import os
ENDING_MARKER = re.compile(ur"[\.\;\?\!]*$",re.UNICODE)
DIGIT = re.compile(ur"\d")
REMOVE_CHAR = re.compile(ur"[\"\(\)\?\:\“]",re.UNICODE)
cdir = os.path.abspath(os.path.dirname(__file__))


def load_vn_vocab():
    from vocabulary import DomainVocaburaly
    vocab = DomainVocaburaly()
    vocab.init()
    return vocab.true_univocab

def load_hard_fixing():
    cdir = os.path.abspath(os.path.dirname(__file__))

    f = open("%s/models/data/inp/common_fixing"%cdir,"r",encoding="utf-8")
    fixing_map = dict()
    while True:
        line = f.readline()
        if line == "":
            break
        if line.startswith("#"):
            continue
        line = line.strip()
        line = unicodedata.normalize('NFC', line)
        parts = line.split("\t")
        if len(parts) >=2:
            fixing_map[parts[0]] = parts[1]
    f.close()
    return fixing_map
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
    sen = sen.replace(u'xa0',u' ')
    sen = sen.strip()
    tokens = sen.split(u" ")
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

    return ENDING_MARKER.sub("",token2)


def extract_wrong_words():
    vn_vocab = load_vn_vocab()
    print len(vn_vocab)
    #fixing_map = load_hard_fixing()
    cc = []
    for c in cc:
        if not c in vn_vocab:
            print "Wrong",c
        #exit(-1)
    wrong_words_counters = dict()
    from data_loader import get_fpt_mobile_data_file_reader
    q_reader = get_fpt_mobile_data_file_reader()
    q = q_reader.readline()
    cc = 0
    while q != "":
        cc += 1
        if cc %100 == 0:
            print "\r%s"%cc,
        q = q.strip()
        q = unicode(q).lower()
        #print q
        tokens = split_sentece(q)
        for token in tokens:

            token = norm_token(token)

            if is_skip_token(token):
                continue

            else:
                if not token in vn_vocab:
                    try:
                        wrong_words_counters[token] += 1
                    except:
                        wrong_words_counters[token] = 1
        q = q_reader.readline()

    q_reader.close()

    kvs = []
    print len(wrong_words_counters)
    for key, value in sorted(wrong_words_counters.iteritems(), key=lambda (k, v): (v, k)):
        kvs.append([key, value])
        #print key,value
    TOP = 1000
    TOP = min(TOP,len(kvs))
    f = open("%s/data/stats/popular_wrong_words.dat"%cdir,"w",encoding="utf-8")
    for i in xrange(1,TOP):
        f.write(u"%s\n"%kvs[-i][0])
        #print kvs[-i][0],kvs[-i][1]
    f.close()


def get_candidate(k2,candidates,ref_scores=None):
    k = spelling_corrector.domain_corrector.text_utils.accent2bare(k2)
    l_bares = []
    for c in candidates:
        l_bares.append(spelling_corrector.domain_corrector.text_utils.accent2bare(c))

    dc = len(k)*1.0
    l_sims = []
    i = -1
    for bare in l_bares:
        i += 1
        count = len(utils.lcs(k,bare))*1.0
        if k2[0] == candidates[i][0]:
            count += 0.1

        count += math.log(100.0+ref_scores[i])/math.log(1000)

        l_sims.append(count/dc)

    #print l_sims

    sorted_scores,sorted_indices = utils.sort_array_indices(l_sims)
    l_true_candidates = []
    for ind in sorted_indices:
        l_true_candidates.append(candidates[ind])
    return l_true_candidates,sorted_scores


def fix_wrong_words_heuristic(data="",path=""):
    vn_vocab = load_vn_vocab()
    fixing_map = load_hard_fixing()
    #hard_regex = HardRegex()
    #hard_regex.load_from_file()
    cc = []
    for c in cc:
        if not c in vn_vocab:
            print "Wrong",c
        #exit(-1)
    wrong_words_counters = dict()
    from data_loader import get_fpt_mobile_data_file_reader
    q_reader = get_fpt_mobile_data_file_reader()

    f_fix = open("%s/data/out/fixing"%cdir,"w",encoding="utf-8")
    bi_forward = dict()
    bi_backward = dict()
    question_norm1 = []

    q = q_reader.readline()
    while q != "":
        qs = q.strip()
        qs = unicode(qs)
        qs = qs.lower()
        #qs = hard_regex.replace(qs)
        tokens = split_sentece(qs)
        qq = []
        ii = -1
        for token in tokens:
            ii += 1
            token = norm_token(token)
            try:
                token = fixing_map[token]
                qq.append(token)
                continue
            except:
                pass
            if is_skip_token(token):
                continue


            else:
                if not token in vn_vocab:
                    #if token == u"luc":
                    #    print "LUC here ",qs
                    try:
                        if ii > 0:
                            #if tokens[ii-1] == u"cường":
                            #    print "\t",token
                            try:
                                bi_backward[token][tokens[ii-1]] += 1
                            except:
                                try:
                                    mm = bi_backward[token]
                                except:
                                    mm = dict()
                                    bi_backward[token] = mm

                                try:
                                    mm[tokens[ii-1]] += 1
                                except:
                                    mm[tokens[ii-1]] = 1
                        if ii < len(tokens) - 1:
                            try:
                                mm = bi_forward[token]
                            except:
                                mm = dict()
                                bi_forward[token] = mm

                            try:
                                mm[tokens[ii + 1]] += 1
                            except:
                                mm[tokens[ii + 1]] = 1

                        wrong_words_counters[token] += 1
                    except:
                        wrong_words_counters[token] = 1
            qq.append(token)


        ss = " ".join(qq)

        question_norm1.append(qq)
        f_fix.write(u"%s\n"%ss)
        q = q_reader.readline()
    f_fix.close()
    kvs = []

    for key, value in sorted(wrong_words_counters.iteritems(), key=lambda (k, v): (v, k)):
        kvs.append([key, value])

    TOP = 400
    f = open("%s/data/out/popular_wrong_words.dat"%cdir,"w",encoding="utf-8")
    for i in xrange(1,TOP):
        f.write(u"%s\n"%kvs[-i][0])
        #print kvs[-ie WMT’14 English to French][0],kvs[-i][1]
    f.close()
    #TOP = 300
    candidates_f = dict()
    candidates_b = dict()


    revert_f = dict()
    revert_b = dict()
    T_TOP = 2
    T_MIN = 8

    f_forward_exist = dict()
    f_backward_exist = dict()
    for i in xrange(1,TOP):
        k = kvs[-i][0]
        #print kvs[-i][0],kvs[-i][1]

        forward_exist = True
        backward_exist = True
        try:

            f_forward = utils.sort_dict(bi_forward[k])
        except:
            forward_exist = False

        try:
            f_backward = utils.sort_dict(bi_backward[k])
        except:
            backward_exist = False

        f_forward_exist[k] = forward_exist
        f_backward_exist[k] = backward_exist

        if forward_exist:
            sz = min(T_TOP,len(f_forward))
            for i in xrange(sz):
                if f_forward[i][1] > T_MIN:
                    try:
                        #print f_forward[i][0]
                        revert_f[f_forward[i][0]].add(k)
                    except:
                        revert_f[f_forward[i][0]] = set()
                        revert_f[f_forward[i][0]].add(k)
        if backward_exist:
            sz = min(T_TOP,len(f_backward))
            for i in xrange(sz):
                if f_backward[i][1] > T_MIN:
                    try:
                        revert_b[f_backward[i][0]].add(k)
                    except:
                        revert_b[f_backward[i][0]] = set()
                        revert_b[f_backward[i][0]].add(k)

    #print revert_b
    #print revert_f

    b_stores = dict()
    f_stores = dict()


    for q in question_norm1:
        i = -1
        for token in q:
            i += 1
            if i < len(q) - 1:
                w_next = q[i+1]
                if w_next in vn_vocab:
                    try:
                        b_own = revert_b[token]
                        #Saving backward word context
                        try:
                            bb = b_stores[w_next]
                        except:
                            bb = dict()
                            b_stores[w_next] = bb
                        try:
                            bb[token] += 1
                        except:
                            bb[token] = 1

                        #Adding to the bw candidates

                        for w in b_own:
                            try:
                                d_cand = candidates_b[w]
                            except:
                                d_cand = dict()
                                candidates_b[w] = d_cand
                            try:
                                d_cand[w_next] += 1
                            except:
                                d_cand[w_next] = 1


                    except:
                        pass
            if i > 0:

                w_before = q[i - 1]

                if w_before in vn_vocab:
                    try:
                        b_own = revert_f[token]
                        try:
                            ff = f_stores[w_before]
                        except:
                            ff = dict()
                            f_stores[w_before] = ff

                        try:
                            ff[token] += 1
                        except:
                            ff[token] = 1

                        for w in b_own:
                            try:
                                d_cand = candidates_f[w]
                            except:
                                d_cand = dict()
                                candidates_f[w] = d_cand
                            try:
                                d_cand[w_before] += 1
                            except:
                                d_cand[w_before] = 1


                    except:
                        pass

    f = open("%s/data/out/fix_candidates"%cdir,"w",encoding="utf-8")
    one_fix = dict()
    f_one_fix = open("%s/data/out/one_fix.dat"%cdir,"w",encoding="utf-8")
    f_multi_fix = open("%s/data/out/multi_fix.dat"%cdir,"w",encoding="utf-8")
    N_MULTI = 2
    N_CONTEXT = 3
    THRES_2  = 0.7

    for k,v in b_stores.iteritems():
        v = utils.sort_dict(v)
        b_stores[k] = v
    for k,v in f_stores.iteritems():
        v = utils.sort_dict(v)
        f_stores[k] = v

    for k,v in candidates_b.iteritems():
        if f_backward_exist[k]:
            #print "Error_b: ",k

            ss = utils.sort_dict(v)
            #print "\t",ss

            ll = []
            l_candidates = []
            l_ref_scores = []
            for s in ss:
                ll.append(u"%s:%s " % (s[0], s[1]))
                l_candidates.append(s[0])
                l_ref_scores.append(s[1])

            ll = " ".join(ll)
            f.write(u"%s:\n" % k)
            f.write(u"\t%s\n" % ll)

            true_candidates,sorted_socre = get_candidate(k,l_candidates,l_ref_scores)

            ll2 = []
            for i in xrange(len(true_candidates)):
                ll2.append(u"%s:%s "%(true_candidates[i],sorted_socre[i]))
            f.write(u"\t%s\n"%" ".join(ll2))

            #Write one fix:
            if sorted_socre[1] < 1 and sorted_socre[0] > 1:
                one_fix[k] = true_candidates[0]
            elif sorted_socre[1] > THRES_2:
                for i in reversed(xrange(2)):
                    fix = true_candidates[i]

                    try:
                        ll_context = []
                        back_context = b_stores[fix]
                        for i in xrange(N_CONTEXT):
                            ll_context.append(back_context[i][0])
                        f_multi_fix.write("B\t%s\t%s\t%s\n"%(k,fix," ".join(ll_context)))
                    except:
                        pass

    f.write(u"\n\n\n")
    for k,v in candidates_f.iteritems():
        if f_forward_exist[k]:
            #print "Error_f: ",k
            ss = utils.sort_dict(v)
            #print "\t",ss

            ll = []
            l_candidates = []
            l_ref_scores = []
            for s in ss:
                ll.append(u"%s:%s " % (s[0], s[1]))
                l_candidates.append(s[0])
                l_ref_scores.append(s[1])
            ll = " ".join(ll)
            f.write(u"%s:\n" % k)
            f.write(u"\t%s\n" % ll)

            true_candidates,sorted_socre = get_candidate(k,l_candidates,l_ref_scores)
            ll2 = []
            for i in xrange(len(true_candidates)):
                ll2.append(u"%s:%s "%(true_candidates[i],sorted_socre[i]))
            f.write(u"\t%s\n"%" ".join(ll2))
            #one fix:
            if sorted_socre[1] < 1 and sorted_socre[0] > 1:
                one_fix[k] = true_candidates[0]
            elif sorted_socre[1] > THRES_2:
                for i in reversed(xrange(2)):
                    fix = true_candidates[i]

                    try:
                        ll_context = []
                        forward_context = f_stores[fix]
                        for i in xrange(N_CONTEXT):
                            ll_context.append(forward_context[i][0])
                        f_multi_fix.write("F\t%s\t%s\t%s\n" % (k, fix, " ".join(ll_context)))
                    except:
                        pass

    f.close()
    for k,v in one_fix.iteritems():
        f_one_fix.write("%s\t%s\n"%(k,v))
    f_one_fix.close()
    f_multi_fix.close()
def test():
    s=u"chào gia"
    s = unicodedata.normalize("NFKC",s)
    parts = s.split(" ")
    print parts
    ss = split_sentece(s)
    print ss
if __name__ == "__main__":
    #fix_wrong_words_heuristic()
    extract_wrong_words()
    #test()