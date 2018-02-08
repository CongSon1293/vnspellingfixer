# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import editdistance

import utils
import math
import os
import stats_bare_bigram
from unigram_fixing import UnigramFixing
class BigramFixing():
    def __init__(self):
        self.cdir = os.path.abspath(os.path.dirname(__file__))
        self.unigram_fixing = UnigramFixing()
        self.vn_vocab, self.vn_bare_vocab, self.vn_long_vocab, self.vn_long_bare_vocab \
            = stats_bare_bigram.load_vn_vocab()
        self.vn_special_words = stats_bare_bigram.load_special_words()
        self.vn_true_bare_bigram_hie_ddict = utils.pickle_load("%s/models/data/out/hierachical_true_dict.pkl"%self.cdir)
        self.vn_true_bare_bigram_f_ddict = utils.pickle_load("%s/models/data/out/hierachical_true_first_ab_dict.pkl"%self.cdir)

        self.hard_fixing_map = stats_bare_bigram.load_hard_fixing()
        self.load_one_fix()
    def load_one_fix(self,path="models/data/out/rule_one_fix.dat"):
        path = "%s/%s"%(self.cdir,path)
        f = open(path,"r",encoding="utf-8")
        self.one_fix_map = dict()
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            parts = line.split(" : ")
            if len(parts) != 2:
                continue
            reg = re.compile(ur"\b%s\b"%parts[0],re.UNICODE)
            self.one_fix_map[reg] = parts[1]
    def save(self,path="models/bigramfixing.dat"):
        path  = "%s/%s"%(self.cdir,path)
        utils.pickle_save(self,path)
    @staticmethod
    def load(path="models/bigramfixing.dat"):
        dir = os.path.abspath(os.path.dirname(__file__))
        path = "%s/%s"%(dir,path)
        return utils.pickle_load(path)
    @staticmethod
    def train(data="",path=""):
        print "Training..."
        from vnnorm_stats_unibi import fix_wrong_words_heuristic
        print "\t Unigram stats..."
        fix_wrong_words_heuristic(data,path)
        print "\t Bigram stast..."
        from stats_bare_bigram import stats_bigram,stats
        stats(data,path,using_news=True)
        stats_bigram()
        print "\t Creating model..."
        bigram = BigramFixing()
        bigram.save()

    def fix(self,sen2):
        qs = sen2
        if qs == None:
            return
        try:
            qs = unicode(qs,encoding="utf-8")
        except:
            pass
        qs = qs.lower()
        qs = self.unigram_fixing.fix(qs)

        qs = stats_bare_bigram.norm_fix_common(qs, self.one_fix_map)
        _tokens = stats_bare_bigram.split_sentece(qs)



        back_ref = " ".join(_tokens)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)
        for reg,repl in self.one_fix_map.iteritems():
            bare_raw_sen = reg.sub(repl,bare_raw_sen)

        for i in xrange(len(tokens)-1):
            bigram = u"%s %s"%(tokens[i],tokens[i+1])
            #print "\t%s"%bigram
            if stats_bare_bigram.is_wrong_bare_bigram_candidates(bigram, self.vn_bare_vocab, self.vn_special_words):

                #print bigram
                d_candidates = {}

                c = bigram[0]
                #self.vn_true_bare_bigram_f_ddict

                #for c in set(bigram):
                if c == " ":
                    continue
                try:
                    sub_dict = self.vn_true_bare_bigram_hie_ddict[c]
                except:
                    continue

                for candidate, counter in sub_dict.iteritems():
                    try:
                        d_candidates[candidate]
                    except:
                        sim_score = stats_bare_bigram.cal_sim_score(bigram, candidate, counter)
                        if sim_score < 0.7:
                            continue
                        d_candidates[candidate] = stats_bare_bigram.cal_sim_score(bigram, candidate, counter)

                if len(d_candidates) == 0:
                    continue
                sorted_score = utils.sort_dict(d_candidates)

                print sorted_score

                if sorted_score[0][1] > 1:# and sorted_score[1][1] < 1:
                    repl = sorted_score[0][0]
                    reg = re.compile(r"\b%s\b"%bigram,re.UNICODE)
                    bare_raw_sen = reg.sub(repl,bare_raw_sen)
        return bare_raw_sen,back_ref


def loop():
    bi_gram_fixing = BigramFixing()

    print "Loading model completed"

    while True:
        inp = raw_input("Enter sentence: ")
        if len(inp)<2:
            print "Invalid input"
            continue
        fixed_sen,back_ref = bi_gram_fixing.fix(inp)
        print u"\tBare norm: %s"%fixed_sen
        print u"\tAccent ref: %s"%back_ref
def fix_question():
    bi_gram_fixing = BigramFixing()
    from load_data import load_questions
    questions = load_questions()

    f = open("stats/bare_question_fixing.dat","w",encoding="utf-8")
    cc = 0
    for qs in questions:
        # print qs
        cc += 1
        print "\r%s"%cc,
        if qs == None or qs == "":
            continue
        try:
            fixed_bare,fix_accent = bi_gram_fixing.fix(qs)
            f.write(u"%s | %s | %s\n"%(fixed_bare,qs,fix_accent))
        except:
            continue
    f.close()
    f.write("\n Done")

if __name__ == "__main__":
    print "Training..."
    BigramFixing.train()
    #bigram = BigramFixing.load()
    bigram = BigramFixing()
    bigram.save()
    #loop()
    #fix_question()
    # bi_gram_fixing = BigramFixing()
    sen = u"Điện thoại này có kinh cường lực ko"
    fixed_sen,back_ref = bigram.fix(sen)
    print sen
    print fixed_sen
    print back_ref