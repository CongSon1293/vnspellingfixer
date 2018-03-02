# -*- coding: utf-8 -*-

import os
import re
import unicodedata
from io import open

import utils

cdir = os.path.abspath(os.path.dirname(__file__))


ENDING_MARKER = re.compile(ur"[\,\.\;\?\!]*$",re.UNICODE)
DIGIT = re.compile(ur"\d")
REMOVE_CHAR = re.compile(ur"[\"\(\)\?\:\“]",re.UNICODE)
MISS_SPACE = re.compile(ur"(?P<BF>\w)(?P<GG>,)(?P<AT>\w)",re.UNICODE)
DMIN = 5


class Vocaburaly():

    def __init__(self):

        #Single vocab:
        #True
        self.true_single_accent_vocab = dict()
        self.true_single_bare_vocab = dict()

        # Total long
        self.true_long_accent_vocab = dict()
        self.true_long_bare_vocab = dict()

        #Biword vocab
        #True
        self.true_bi_accent_vocab = dict()
        self.true_bi_bare_vocab = dict()
        #Stats
        self.all_bi_accent_vocab = dict()
        self.all_bi_bare_vocab = dict()

    def init(self):
        self.__load_true_vocab()
        self.__load_all_news_bi_words()
        self.__load_all_subtitles_bi_words()
        self.__merge_bigram_counter()

    def split_dot(self,token):
        res = []
        if DIGIT.search(token) == None:
            parts = token.split(".")
            for p in parts:
                if len(p) > 0:
                    res.append(p)
        else:
            res.append(token)
        return res

    def split_sentece(self,sen):
        tokens = sen.split(" ")
        res = []
        for token in tokens:
            ss = self.split_dot(token)
            for s in ss:
                res.append(s)
        return res

    def is_skip_token(self,token):
        if len(token) < 2:
            return True
        for c in token:
            if c.isdigit():
                return True
        if token.__contains__(",") or token.__contains__(".."):
            return True
        return False

    def norm_token(self,token):
        token2 = unicodedata.normalize('NFC', token)
        token2 = REMOVE_CHAR.sub("", token2)
        token2 = MISS_SPACE.sub(ur"\g<BF>\g<GG> \g<AT>", token2)
        return ENDING_MARKER.sub("", token2)

    def add_true_vocab(self,full_word):
        full_word = unicodedata.normalize('NFC', full_word)
        utils.add_dict_counter(self.true_long_accent_vocab, full_word)
        utils.add_dict_counter(self.true_long_bare_vocab, utils.accent2bare(full_word))
        words = full_word.split(" ")

        for word in words:
            utils.add_dict_counter(self.true_single_accent_vocab, word)
            utils.add_dict_counter(self.true_single_bare_vocab, utils.accent2bare(word))

        if len(words) == 2:
            utils.add_dict_counter(self.true_bi_accent_vocab, full_word)
            utils.add_dict_counter(self.true_bi_bare_vocab, utils.accent2bare(full_word))

    def __load_true_vocab(self):
        f = open("%s/../resources/vocab/full_vocaburaly.txt" % cdir, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            full_word = line.strip().lower()
            self.add_true_vocab(full_word)

        f.close()

        f = open("%s/../resources/vocab/missing_vocab" % cdir, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            word = unicodedata.normalize("NFC", line.strip())
            self.add_true_vocab(word)
        f.close()

    def __load_all_subtitles_bi_words(self):
        subtitle_bigram = {}
        from data_loader import get_subtitle_reader
        subtitle_reader = get_subtitle_reader()
        cc = 0
        print "Loading subtitle bigrams..."
        line  = subtitle_reader.readline()
        while line != "":
            cc += 1
            if cc %100 == 0:
                print "\r\t\t\t%s"%cc,
            if cc >=10000000:
                break
            line = line.strip()
            qs = line.lower()
            tokens = []
            _tokens = self.split_sentece(qs)
            for token in _tokens:
                token = utils.accent2bare(token)
                tokens.append(token)

            for i in xrange(len(tokens)):
                if i < len(tokens) - 1:
                    utils.add_dict_counter(subtitle_bigram, u"%s %s" % (tokens[i], tokens[i + 1]))
            line = subtitle_reader.readline()
        subtitle_reader.close()

        print "\t\t: Subtitles stats:"
        print "\t\t: Have %s bigrams" % len(subtitle_bigram)
        self.subtitle_bigram = utils.fitler_dict_couter(subtitle_bigram, DMIN)

        print "\t\t: After fitlering: %s" % len(self.subtitle_bigram)

    def __load_all_news_bi_words(self):
        news_bigram = {}
        from data_loader import get_news_sentence_reader
        sentences_reader = get_news_sentence_reader()
        line = sentences_reader.readline()
        cc = 0
        print "Loading news bigrams"
        while line != "":
            cc += 1
            if cc % 100 == 0:
                print "\r\t\t\t%s" % cc,
            if cc >= 600000:
                break
            line = line.strip()
            qs = line.lower()
            #qs = norm_fix_common(qs, fixing_map)
            _tokens = self.split_sentece(qs)

            tokens = []
            for token in _tokens:
                token = utils.accent2bare(token)
                tokens.append(token)

            for i in xrange(len(tokens)):
                if i < len(tokens) - 1:
                    utils.add_dict_counter(news_bigram, u"%s %s" % (tokens[i], tokens[i + 1]))

            line = sentences_reader.readline()
        sentences_reader.close()

        print "\t\t: News stats:"
        print "\t\t: Have %s bigrams" % len(news_bigram)
        self.news_bigram_counter = utils.fitler_dict_couter(news_bigram, DMIN)

        print "\t\t: After fitlering: %s" % len(self.news_bigram_counter)
        #self.hierachical_first_char_dict = utils.generate_hierachical_first_alphabet_dict(self.news_bigram_counter)
    def __merge_bigram_counter(self):
        self.news_bigram_counter = utils.merge_counting_dict(self.news_bigram_counter,
                                                             self.subtitle_bigram)
        self.hierachical_first_char_dict = utils.generate_hierachical_first_alphabet_dict(self.news_bigram_counter)
    def load_extended_true_bivocab(self,path="models/data/inp/extended_bivocab.dat"):
        path = "%s/%s"%(cdir,path)
        f = open(path,"r")
        while True:
            line = f.readline()
            if line == "":
                break
            word = line.strip().lower()
            utils.add_dict_counter(self.true_bi_accent_vocab, word)
            utils.add_dict_counter(self.true_bi_bare_vocab, utils.accent2bare(word))

            #utils.add_dict_counter(self.news_bigram_counter,word,100)
            #self.hierachical_first_char_dict = utils.generate_hierachical_first_alphabet_dict(self.news_bigram_counter)
        f.close()

    def save(self,path="models/model_vocab.pkl"):
        path = "%s/%s"%(cdir,path)
        utils.pickle_save(self, path)
    @staticmethod
    def load(path="models/model_vocab.pkl"):
        path = "%s/%s" % (cdir, path)
        print "Loading vocab data from %s"%path
        return utils.pickle_load(path)

    def check_true_single_accent_vocab(self,word):

        return utils.get_zero_dict(self.true_single_accent_vocab, word)

    def check_true_single_bare_vocab(self,word,skip_digit=True,new_true_vocab=""):
        if skip_digit:
            if DIGIT.search(word) != None:
                return 1
        if new_true_vocab != "":
            if type(new_true_vocab) == set:
                if word in new_true_vocab:
                    return 1
                else:
                    return 0
            else:
                try:
                    new_true_vocab[word]
                    return 1
                except:
                    return 0
        return utils.get_zero_dict(self.true_single_bare_vocab, word)

    def check_true_bi_bare_vocab(self,word):
        return utils.get_zero_dict(self.true_bi_bare_vocab, word)

