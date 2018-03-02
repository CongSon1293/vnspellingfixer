# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open

from text_utils import *
from vocabulary import DomainVocaburaly
import os
import sys
sys.path.insert(0, '..')
from spelling_corrector.general_bare_corrector.similarity_metrics import cal_sim_score,cal_sim_score_2
cdir = os.path.abspath(os.path.dirname(__file__))

WRONG_UNIGRAM_STATS_FILE = "data/stats/wrong_unigrams.stats"
TOP = 1000


class WrongUnigramStats():

    def __init__(self):

        self.__domain_vocab = DomainVocaburaly()
        self.__domain_vocab.init()
        self.__true_univocab = self.__domain_vocab.true_univocab
        self.__out_file = WRONG_UNIGRAM_STATS_FILE
    #First step
    def export_wrong_words(self):
        print "Stats wrong unigram..."

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
            q = q.lower()
            tokens = split_sentece(q)
            for token in tokens:

                token = norm_token(token)
                if is_skip_token(token):
                    continue
                else:
                    if not token in self.__true_univocab:
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
        R_TOP = min(TOP,len(kvs))
        f = open("%s/%s"%(cdir,self.__out_file),"w",encoding="utf-8")
        for i in xrange(1,R_TOP):
            f.write(u"%s\n"%kvs[-i][0])
        f.close()


class StatsOneRuleUnigram():
    def __init__(self):
        self.__domain_vocab = DomainVocaburaly()
        self.__domain_vocab.init()
        self.__true_univocab = self.__domain_vocab.true_univocab

        self.__fix_unigram_candidates_file = "%s/data/stats/fix_candidates" % cdir
        self.__unigram_fix_rules_file = "%s/data/stats/uni_fix.dat" % cdir
        self.__unigram_fix_multi_rules_file = "%s/data/stats/multi_fix.dat" % cdir
    def get_candidate(self,k2, candidates, ref_scores=None):

        k = accent2bare(k2)
        l_bares = []
        for c in candidates:
            l_bares.append(accent2bare(c))
        l_sims = []
        i = -1
        for bare in l_bares:
            i += 1
            l_sims.append(cal_sim_score_2(k,bare,ref_scores[i]))
        sorted_scores, sorted_indices = utils.sort_array_indices(l_sims)
        l_true_candidates = []
        for ind in sorted_indices:
            l_true_candidates.append(candidates[ind])
        return l_true_candidates, sorted_scores


    def fix_wrong_words_heuristic(self):

        wrong_words_counters = dict()
        from data_loader import get_fpt_mobile_data_file_reader
        q_reader = get_fpt_mobile_data_file_reader()

        f_fix = open("%s/data/out/fixing" % cdir, "w", encoding="utf-8")
        bi_forward = dict()
        bi_backward = dict()
        question_norm1 = []

        q = q_reader.readline()
        cc = 0
        while q != "":
            cc += 1
            if cc %100==0:
                print "\r%s"%cc,
            qs = q.strip()
            qs = qs.lower()
            tokens = split_sentece(qs)
            qq = []
            ii = -1
            for token in tokens:
                ii += 1
                token = norm_token(token)
                if is_skip_token(token):
                    continue


                else:
                    if not token in self.__true_univocab:
                        try:
                            if ii > 0:
                                try:
                                    bi_backward[token][tokens[ii - 1]] += 1
                                except:
                                    try:
                                        mm = bi_backward[token]
                                    except:
                                        mm = dict()
                                        bi_backward[token] = mm

                                    try:
                                        mm[tokens[ii - 1]] += 1
                                    except:
                                        mm[tokens[ii - 1]] = 1
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
            f_fix.write(u"%s\n" % ss)
            q = q_reader.readline()
        f_fix.close()
        kvs = []

        for key, value in sorted(wrong_words_counters.iteritems(), key=lambda (k, v): (v, k)):
            kvs.append([key, value])

        TOP = 400
        f = open("%s/%s" % (cdir,WRONG_UNIGRAM_STATS_FILE), "w", encoding="utf-8")
        for i in xrange(1, TOP):
            f.write(u"%s\n" % kvs[-i][0])
        f.close()
        candidates_f = dict()
        candidates_b = dict()

        revert_f = dict()
        revert_b = dict()
        T_TOP = 2
        T_MIN = 8

        f_forward_exist = dict()
        f_backward_exist = dict()
        for i in xrange(1, TOP):
            k = kvs[-i][0]
            # print kvs[-i][0],kvs[-i][1]

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
                sz = min(T_TOP, len(f_forward))
                for i in xrange(sz):
                    if f_forward[i][1] > T_MIN:
                        try:
                            # print f_forward[i][0]
                            revert_f[f_forward[i][0]].add(k)
                        except:
                            revert_f[f_forward[i][0]] = set()
                            revert_f[f_forward[i][0]].add(k)
            if backward_exist:
                sz = min(T_TOP, len(f_backward))
                for i in xrange(sz):
                    if f_backward[i][1] > T_MIN:
                        try:
                            revert_b[f_backward[i][0]].add(k)
                        except:
                            revert_b[f_backward[i][0]] = set()
                            revert_b[f_backward[i][0]].add(k)

        # print revert_b
        # print revert_f

        b_stores = dict()
        f_stores = dict()

        for q in question_norm1:
            i = -1
            for token in q:
                i += 1
                if i < len(q) - 1:
                    w_next = q[i + 1]
                    if w_next in self.__true_univocab:
                        try:
                            b_own = revert_b[token]
                            # Saving backward word context
                            try:
                                bb = b_stores[w_next]
                            except:
                                bb = dict()
                                b_stores[w_next] = bb
                            try:
                                bb[token] += 1
                            except:
                                bb[token] = 1

                            # Adding to the bw candidates

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

                    if w_before in self.__true_univocab:
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

        f = open(self.__fix_unigram_candidates_file, "w", encoding="utf-8")
        one_fix = dict()
        f_one_fix = open(self.__unigram_fix_rules_file, "w", encoding="utf-8")
        f_multi_fix = open(self.__unigram_fix_multi_rules_file, "w", encoding="utf-8")
        N_MULTI = 2
        N_CONTEXT = 3
        THRES_2 = 0.7

        for k, v in b_stores.iteritems():
            v = utils.sort_dict(v)
            b_stores[k] = v
        for k, v in f_stores.iteritems():
            v = utils.sort_dict(v)
            f_stores[k] = v

        for k, v in candidates_b.iteritems():
            if f_backward_exist[k]:
                # print "Error_b: ",k

                ss = utils.sort_dict(v)
                # print "\t",ss

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

                true_candidates, sorted_socre = self.get_candidate(k, l_candidates, l_ref_scores)

                ll2 = []
                for i in xrange(len(true_candidates)):
                    ll2.append(u"%s:%s " % (true_candidates[i], sorted_socre[i]))
                f.write(u"\t%s\n" % " ".join(ll2))

                # Write one fix:
                if len(sorted_socre) == 1 or (sorted_socre[1] < 1 and sorted_socre[0] > 1):
                    one_fix[k] = true_candidates[0]
                elif sorted_socre[1] > THRES_2:
                    for i in reversed(xrange(2)):
                        fix = true_candidates[i]

                        try:
                            ll_context = []
                            back_context = b_stores[fix]
                            for i in xrange(N_CONTEXT):
                                ll_context.append(back_context[i][0])
                            f_multi_fix.write("B\t%s\t%s\t%s\n" % (k, fix, " ".join(ll_context)))
                        except:
                            pass

        f.write(u"\n\n\n")
        for k, v in candidates_f.iteritems():
            if f_forward_exist[k]:
                # print "Error_f: ",k
                ss = utils.sort_dict(v)
                # print "\t",ss

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

                true_candidates, sorted_socre = self.get_candidate(k, l_candidates, l_ref_scores)
                ll2 = []
                for i in xrange(len(true_candidates)):
                    ll2.append(u"%s:%s " % (true_candidates[i], sorted_socre[i]))
                f.write(u"\t%s\n" % " ".join(ll2))
                # one fix:
                if len(sorted_socre)==1 or (sorted_socre[1] < 1 and sorted_socre[0] > 1):
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
        for k, v in one_fix.iteritems():
            f_one_fix.write("%s\t%s\n" % (k, v))
        f_one_fix.close()
        f_multi_fix.close()

class BareBigramStats():
    def __init__(self):
        self.__domain_vocab = DomainVocaburaly()
        self.__domain_vocab.init()
        self.__bare_bigram_file = "%s/data/stats/bare_bigrams.stats"%cdir
        self.__bare_bigram_candidates = "%s/data/stats/bare_bigrams_candidats.stats"%cdir
        self.__bare_bigram_fixing_rules = "%s/data/stats/bigram_fix.dat"%cdir

    def export_bare_bigram_stats(self):
        from rules_fixing import RulesFixing
        hard_fixing = RulesFixing()
        hard_fixing.init(level=1)
        from data_loader import get_fpt_mobile_data_file_reader
        import text_utils
        q_reader = get_fpt_mobile_data_file_reader()

        bare_bigram_counter = {}


        q = q_reader.readline()
        cc = 0
        while q != "":
            cc += 1
            if cc % 100 == 0:
                print "\r%s" % cc,
            qs = q.strip()
            qs = qs.lower()
            qs = hard_fixing.fix(qs)

            _tokens = split_sentece(qs)
            tokens = []
            for token in _tokens:
                token = norm_token(token)
                #if is_skip_token(token):
                #    continue
                token = text_utils.accent2bare(token)
                tokens.append(token)
            for i in xrange(len(tokens)-1):
                bare_bigram = "%s %s"%(tokens[i],tokens[i+1])
                utils.add_dict_counter(bare_bigram_counter,bare_bigram)

            q = q_reader.readline()

        q_reader.close()
        print "\nHave %s bigrams"%len(bare_bigram_counter)
        bare_bigram_none_digit = utils.filter_dict_digitkey(bare_bigram_counter)
        bare_bigram_counter_filtered = utils.fitler_dict_couter(bare_bigram_none_digit,2)
        print "After filtering: %s"%len(bare_bigram_counter_filtered)
        utils.pickle_save(bare_bigram_counter_filtered,self.__bare_bigram_file)
    def __is_wrong_bare_bigram(self,bare_bigram):

            if self.__domain_vocab.is_special_bare_bigram(bare_bigram):
                    return False

            tokens = bare_bigram.split(" ")
            #if DIGIT.search(bare_bigram) != None:
            #    return False
            for tk in tokens:
                if not self.__domain_vocab.is_valid_bare_token(tk):
                    return True
            return False

    def stats_bigram_hardfixing(self):
        bigrams_counter = utils.pickle_load(self.__bare_bigram_file)
        true_bigram_candidates = {}
        wrong_bigram_candidates = {}

        for bigram, counter in bigrams_counter.iteritems():
            if self.__is_wrong_bare_bigram(bigram):
                if counter > 5:
                    wrong_bigram_candidates[bigram] = counter
            else:
                if counter > 8:
                    true_bigram_candidates[bigram] = counter

        print "Wrong candidate size: %s" % len(wrong_bigram_candidates)
        print "Fixing candidate size: %s" % len(true_bigram_candidates)
        print "Searching for candidates..."




        hierachical_true_bigram_candidates = utils.generate_hierachical_first_alphabet_dict(true_bigram_candidates)
        f_bigram_fixing = open(self.__bare_bigram_fixing_rules,"w",encoding="utf-8")
        f_bigram_candidats = open(self.__bare_bigram_candidates,"w",encoding="utf-8")
        cc = 0
        for wrong_bigram, counter in wrong_bigram_candidates.iteritems():
            cc += 1
            print "\r%s" % cc,
            d_candidates = {}
            first_char = wrong_bigram[0]
            if first_char == " ":
                continue
            try:
                sub_dict = hierachical_true_bigram_candidates[first_char]
            except:
                continue

            #print wrong_bigram,"F:",first_char,"C:",counter

            for candidate, counter in sub_dict.iteritems():
                #print candidate
                try:
                    d_candidates[candidate]
                except:
                    d_candidates[candidate] = cal_sim_score(wrong_bigram, candidate, counter)

            sorted_score = utils.sort_dict(d_candidates)


            f_bigram_candidats.write(u"%s:\n"%wrong_bigram)

            ss = []
            SZ = min(TOP,len(sorted_score))
            for i in xrange(SZ):
                ss.append("%s:%s " % (sorted_score[i][0], sorted_score[i][1]))
            ss = " ".join(ss)
            if sorted_score[0][1] > 1 and sorted_score[1][1] < 1:
                # print "A Rule"
                f_bigram_fixing.write(u"%s\t%s\n" % (wrong_bigram, sorted_score[0][0]))
                f_bigram_fixing.flush()
            f_bigram_candidats.write(u"\t%s\n" % ss)
        f_bigram_fixing.close()
        f_bigram_candidats.close()
        print "\n\n\tDone"



