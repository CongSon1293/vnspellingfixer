# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import editdistance
import os
import utils
from custom_regex import HardRegex,CommonRegex
import math

cdir = os.path.abspath(os.path.dirname(__file__))

ENDING_MARKER = re.compile(ur"[\,\.\;\?\!]*$",re.UNICODE)
DIGIT = re.compile(ur"\d")
REMOVE_CHAR = re.compile(ur"[\"\(\)\?\:\“]",re.UNICODE)
MISS_SPACE = re.compile(ur"(?P<BF>\w)(?P<GG>,)(?P<AT>\w)",re.UNICODE)
DMIN = 5
cdir = os.path.abspath(os.path.dirname(__file__))


def load_special_words():
    vn_special_words = set()

    f = open("%s/models/data/inp/special_words"%cdir, "r")
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip().lower()
        line = unicodedata.normalize('NFC', line)
        vn_special_words.add(line)
        vn_special_words.add(utils.accent2bare(line))

    f.close()
    return vn_special_words

def load_vn_vocab():
    vn_vocab = set()
    vn_bare_vocab = set()
    vn_long_vocab = set()
    vn_long_bare_vocab = set()

    f = open("%s/models/data/full_vocaburaly.txt"%cdir,"r")
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip().lower()
        line = unicodedata.normalize('NFC',line)
        vn_long_vocab.add(line)
        vn_long_bare_vocab.add(utils.accent2bare(line))
        words = line.split(" ")
        for word in words:
            vn_vocab.add(word)
            vn_bare_vocab.add(utils.accent2bare(word))
    f.close()

    f = open("%s/models/data/inp/special_tokens"%cdir,"r")
    while True:
        line = f.readline()
        if line == "":
            break
        word = unicodedata.normalize("NFC",line.strip())
        vn_vocab.add(word)
        vn_bare_vocab.add(utils.accent2bare(word))
        vn_long_vocab.add(word)
        vn_long_bare_vocab.add(utils.accent2bare(word))
    f.close()
    f = open("%s/models/data/inp/missing_vocab"%cdir,"r")
    while True:
        line = f.readline()
        if line == "":
            break
        word = unicodedata.normalize("NFC",line.strip())
        vn_vocab.add(word)
        vn_bare_vocab.add(utils.accent2bare(word))
        vn_long_vocab.add(word)
        vn_long_bare_vocab.add(utils.accent2bare(word))
    f.close()
    return vn_vocab,vn_bare_vocab,vn_long_vocab,vn_long_bare_vocab


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

def test():
    vn_vocab,vn_bare_vocab,vn_long_vocab,vn_long_bare_vocab \
        =load_vn_vocab()
    print vn_long_bare_vocab


def norm_fix_common(sen,fix_map):
    _tokens = split_sentece(sen)
    fixies = []
    for token in _tokens:
        token = utils.get_dict_element(fix_map,token)
        token2 = norm_token(token)
        token2s_ = split_sentece(token2)
        for tk in token2s_:
            tnorm = norm_token(tk)
            fixies.append(tnorm)
    return " ".join(fixies)


def is_wrong_bare_bigram_candidates(bare_bigram,vn_bare_vocab,vn_speical_words=""):
    if vn_speical_words != "":
        if bare_bigram in vn_speical_words:
            return False

    tokens = bare_bigram.split(" ")
    if DIGIT.search(bare_bigram) != None:
        return False
    for tk in tokens:

        if not tk in vn_bare_vocab:
            return True
    return False
def is_true_bare_bigram(bare_bigram,vn_bare_long_vocab):
    return bare_bigram in vn_bare_long_vocab
def preprocess_sen(sen,fixing_map=""):
    qs = unicode(sen)
    qs = qs.lower()
    qs = norm_fix_common(qs, fixing_map)
    _tokens = split_sentece(qs)

    tokens = []
    for token in _tokens:
        token = utils.accent2bare(token)
        tokens.append(token)

    return tokens

def export_bare_questions():
    from load_data import load_questions
    questions = load_questions()
    fixing_map = load_hard_fixing()

    f = open("out/bare_questions.dat","w")


    for qs in questions:
        # print qs
        qs = unicode(qs)
        qs = qs.lower()
        qs = norm_fix_common(qs, fixing_map)
        _tokens = split_sentece(qs)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)
        sentence = " ".join(tokens)
        f.write(u"%s\n"%sentence)
    f.close()


def stats(data="",path="",using_news=True):
    vn_vocab,vn_bare_vocab,vn_long_vocab,vn_long_bare_vocab \
        =load_vn_vocab()
    fixing_map = load_hard_fixing()
    wrong_words_counters = dict()
    bigram_counters = dict()
    if data != "":
        questions = data
    elif path!="":
        from load_data import load_question_from_file
        load_question_from_file(path)
    else:
        from load_data import load_questions
        questions = load_questions()
    cdir = os.path.abspath(os.path.dirname(__file__))


    for qs in  questions:
        #print qs
        qs = unicode(qs)
        qs = qs.lower()
        qs = norm_fix_common(qs,fixing_map)
        _tokens = split_sentece(qs)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        for i in xrange(len(tokens)):
            if not tokens[i] in vn_bare_vocab:
                utils.add_dict_counter(wrong_words_counters,tokens[i])
            if i < len(tokens) - 1:
                utils.add_dict_counter(bigram_counters,u"%s %s"%(tokens[i],tokens[i+1]))
    if using_news:
        print "\t\tUsing public news data"
        news_bigram = {}
        from load_data import get_news_sentence_reader
        sentences_reader = get_news_sentence_reader()
        line = sentences_reader.readline()
        cc = 0
        while line != "":
            cc += 1
            if cc % 100 == 0:
                print "\r\t\t\t%s"%cc,
            if cc >= 600000:
                break
            line = line.strip()
            qs = line.lower()
            qs = norm_fix_common(qs, fixing_map)
            _tokens = split_sentece(qs)

            tokens = []
            for token in _tokens:
                token = utils.accent2bare(token)
                tokens.append(token)

            for i in xrange(len(tokens)):
                if i < len(tokens) - 1:
                    utils.add_dict_counter(news_bigram, u"%s %s" % (tokens[i], tokens[i + 1]))

            line = sentences_reader.readline()
        sentences_reader.close()
    print "\t\t: Corpus stats:"
    print "\t\t: Have %s bigrams"%len(bigram_counters)
    bigram_counters = utils.fitler_dict_couter(bigram_counters,2)
    print "\t\t: After filtering: %s"%len(bigram_counters)

    print "\t\t: News stats:"
    print "\t\t: Have %s bigrams"%len(news_bigram)
    news_bigram_counter = utils.fitler_dict_couter(news_bigram,DMIN)
    print "\t\t: After fitlering: %s"%len(news_bigram_counter)

    sorted_wrong_tokens = utils.sort_dict(wrong_words_counters)
    sorted_bigram_counter = utils.sort_dict(bigram_counters)
    sorted_news_bigram = utils.sort_dict(news_bigram_counter)
    f_wrong = open("%s/models/data/out/wrong_tokens.dat"%cdir,"w",encoding="utf-8")
    f_bigram_stats = open("%s/models/data/out/bigram_tokens.dat"%cdir,"w",encoding="utf-8")
    f_news_bigram = open("%s/models/data/out/news_bigram_tokens.dat"%cdir,"w",encoding="utf-8")
    for kv in sorted_wrong_tokens:
        ss = DIGIT.search(kv[0])
        if ss != None:
            continue
        f_wrong.write(u"%s : %s\n"%(kv[0],kv[1]))
    f_wrong.close()
    for kv in sorted_bigram_counter:
        f_bigram_stats.write(u"%s : %s\n"%(kv[0],kv[1]))
    f_bigram_stats.close()

    for kv in sorted_news_bigram:
        f_news_bigram.write(u"%s : %s\n"%(kv[0],kv[1]))
    f_news_bigram.close()

def cal_sim_score(src, cand, ref_score=0):
    l = 0.5*(1.0/len(src)+1.0/len(cand))
    l2 = max(len(src),len(cand))
    #count = len(utils.lcs(src, cand)) * 1.0 + 1 - editdistance.eval(src,cand)*l
    count = utils.lcs2(src, cand) * 1.0 + 1.05 +  math.log(1.0/(1.2+ editdistance.eval(src,cand)))

    #count = l - editdistance.eval(src,cand)
    if src[0] == cand[0]:
        count += 0.1
    if ref_score > 0:
        count += math.log(100.0 + ref_score) / math.log(1000)
    return count *l


def generate_hierachical_alphabet_dict(ddict):
    hierachical_dict = {}
    for k,v in ddict.iteritems():
        for c in set(k):
            if c == " ":
                continue
            try:
                d = hierachical_dict[c]
            except:
                d = {}
                hierachical_dict[c] = d
            d[k] = v
    return hierachical_dict
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

def load_sorted_counter_dict(path):
    f = open(path)
    bigram_counters = {}
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip()

        parts = line.split(" : ")

        if len(parts) != 2:
            continue
        bigram = parts[0]
        if DIGIT.search(bigram) != None:
            continue
        cc = int(parts[1])
        bigram_counters[bigram] = cc
    f.close()
    return bigram_counters
def stats_bigram():
    vn_vocab, vn_bare_vocab, vn_long_vocab, vn_long_bare_vocab \
        = load_vn_vocab()
    vn_special_words = load_special_words()
    bigram_counters = load_sorted_counter_dict("%s/models/data/out/bigram_tokens.dat"%cdir)

    news_bigrams = load_sorted_counter_dict("%s/models/data/out/news_bigram_tokens.dat"%cdir)
    wrong_bigram_candidates = {}
    true_bigram_candidates = {}
    for bigram,counter in bigram_counters.iteritems():
        if is_wrong_bare_bigram_candidates(bigram,vn_bare_vocab,vn_special_words):
            if counter > 2:
                wrong_bigram_candidates[bigram] = counter
        else:
            if counter > 8:
                true_bigram_candidates[bigram] = counter

    for bigram,counter in news_bigrams.iteritems():
        cc = utils.get_zero_dict(true_bigram_candidates,bigram)
        cc += counter
        true_bigram_candidates[bigram] = cc

    #Searching for candidates

    f_out = open("%s/models/data/out/bigram_candidates.dat"%cdir,"w",encoding="utf-8")
    f_rules_fix = open("%s/models/data/out/rule_one_fix.dat"%cdir,"w",encoding="utf-8")
    TOP = 10
    #print len(true_bigram_candidates)
    #exit(-1)
    hierachical_true_dict = generate_hierachical_alphabet_dict(true_bigram_candidates)
    hierachical_true_first_ab_dict = generate_hierachical_first_alphabet_dict(true_bigram_candidates)
    utils.pickle_save(hierachical_true_dict,"%s/models/data/out/hierachical_true_dict.pkl"%cdir)
    utils.pickle_save(hierachical_true_first_ab_dict,"%s/models/data/out/hierachical_true_first_ab_dict.pkl"%cdir)
    utils.pickle_save(wrong_bigram_candidates,"%s/models/data/out/wrong_bigrams.pkl"%cdir)
    print "Wrong candidate size: %s"%len(wrong_bigram_candidates)
    print "Fixing candidate size: %s"%len(true_bigram_candidates)
    print "Searching for candidates..."

    cc = 0

    for wrong_bigram,counter in wrong_bigram_candidates.iteritems():
        cc += 1
        print "\r%s"%cc,

        d_candidates = {}

        for c in set(wrong_bigram):
            if c == " ":
                continue
            try:
                sub_dict = hierachical_true_dict[c]
            except:
                continue

            for candidate,counter in sub_dict.iteritems():
                try:
                    d_candidates[candidate]
                except:
                    d_candidates[candidate] = cal_sim_score(wrong_bigram, candidate, counter)

        sorted_score = utils.sort_dict(d_candidates)

        f_out.write(u"%s:\n"%wrong_bigram)
        ss = []
        for i in xrange(TOP):
            ss.append("%s:%s "%(sorted_score[i][0],sorted_score[i][1]))
        ss = " ".join(ss)
        if sorted_score[0][1] > 1 and sorted_score[1][1] < 1:
            #print "A Rule"
            f_rules_fix.write(u"%s : %s\n"%(wrong_bigram,sorted_score[0][0]))
            f_rules_fix.flush()
        f_out.write(u"\t%s\n"%ss)
    f_out.close()
    f_rules_fix.close()
    print "\n\n\tDone"







if __name__ == "__main__":
    stats_bigram()
    #ss = u"hang khong"
    #s2 = u"hag khong"
    #print editdistance.eval(ss,s2)
    #export_bare_questions()