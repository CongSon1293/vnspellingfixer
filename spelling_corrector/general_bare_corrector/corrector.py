# -*- coding: utf-8 -*-

import math
import re

import utils
from general_rules import GeneralRuleFixer
from similarity_metrics import cal_sim_score
from language_model import LanguageModel
import config
from datetime import datetime
N_TOP_CANDIDATES = 4
N_CUTOFF_VALID = 4
SIZE_VARIANT = 4
G_N_TOP_RETURN = 2
R_MARKER_REF = re.compile(ur"(?P<MARKER>[\`\'\^\?\~\*\(\)])")
ACCENT_TEENCODE_REG = re.compile(ur"(?<=\S)[\`\'\^\?\~\*]")
SPLITER_TOKENS = re.compile(ur"$|(\.\.\.)|(\!\!\!)|\.|\,|\?|\!|\;|\(|\)|\|\{|\}|\[|\]|\“|\”",re.UNICODE)
BEGIN_TOKENS = {u"“",u"(",u"{",u"["}
class GeneralBareCorrector():
    def __init__(self,pre_vocab = True):
        print "Initializing GeneralBareCorrector..."
        if not LanguageModel.is_model_existed():
            pre_vocab = False
        if not pre_vocab:
            self.language_model = LanguageModel()
            self.language_model.init()
            #self.vocab.__load_true_vocab()
            #self.vocab.__load_all_news_bi_words()
            self.language_model.save()
        else:
            self.language_model = LanguageModel.load()
            self.language_model.load_extended_true_bivocab()
        self.rule_fix = GeneralRuleFixer()



    def __is_suitable_length(self,word,candidate,size=SIZE_VARIANT):
        if math.fabs(len(word)-len(candidate)) <= SIZE_VARIANT:
            return True
        return False
    def __is_true_biword(self,tokens,current_index,offset):
        start_index = current_index + offset
        if start_index >= 0 and start_index < len(tokens) - 1:
            biword = "%s %s"%(tokens[start_index],tokens[start_index+1])
            return self.language_model.check_true_bi_bare_vocab(biword)
        return False



    def __fix_wrong_candidate(self, wrong_bigram,true_vocab_priority=True):
        d_candidates = {}
        c = wrong_bigram[0]

        if c == " ":
            return wrong_bigram,0
        try:
            sub_dict = self.language_model.hierachical_first_char_dict[c]
        except:
            return wrong_bigram,0

        for candidate, counter in sub_dict.iteritems():
            if not self.__is_suitable_length(wrong_bigram,candidate):
                continue
            try:
                d_candidates[candidate]
            except:
                sim_score = cal_sim_score(wrong_bigram, candidate, counter)
                if sim_score < 0.7:
                    continue
                d_candidates[candidate] = cal_sim_score(wrong_bigram, candidate, counter)

        if len(d_candidates) == 0:
            return wrong_bigram,0
        sorted_score = utils.sort_dict(d_candidates)

        print sorted_score[:3],len(sorted_score)
        VALID_SIZE = min(len(sorted_score),N_TOP_CANDIDATES)

        if true_vocab_priority:
            for i in xrange(VALID_SIZE):
                candidate = sorted_score[i][0]
                if self.language_model.check_true_bi_bare_vocab(candidate):
                    return candidate,sorted_score[i][1]


        if sorted_score[0][1] > config.MIN_CAND_SCORE:
            candidate = sorted_score[0][0]
            return candidate,sorted_score[0][1]

        return wrong_bigram,0

    def __fix_wrong_multi_candidates(self, wrong_bigram,true_vocab_priority=True):

        d_candidates = {}
        c = wrong_bigram[0]

        if c == " ":
            return [wrong_bigram],[0]
        try:

            sub_dict = self.language_model.hierachical_first_char_dict[c]
        except:
            return [wrong_bigram],[0]
        n_cal = 0
        n_val = 0

        for candidate, counter in sub_dict.iteritems():
            if not self.__is_suitable_length(wrong_bigram,candidate):
                continue
            try:
                d_candidates[candidate]
            except:
                sim_score = cal_sim_score(wrong_bigram, candidate, counter)
                n_cal += 1
                if sim_score < 0.7:
                    continue
                if sim_score > 1.0:
                    n_val += 1
                d_candidates[candidate] = cal_sim_score(wrong_bigram, candidate, counter)
                if n_val > N_CUTOFF_VALID:
                    break
        if len(d_candidates) == 0:
            return [wrong_bigram],[0]
        sorted_score = utils.sort_dict(d_candidates)

        print wrong_bigram,sorted_score[:3],len(sorted_score),n_cal

        VALID_SIZE = min(len(sorted_score),N_TOP_CANDIDATES)
        N_TOP_RETURN = G_N_TOP_RETURN
        candidates = []
        scores = []
        if true_vocab_priority:
            for i in xrange(VALID_SIZE):
                candidate = sorted_score[i][0]
                if self.language_model.check_true_bi_bare_vocab(candidate):
                    candidates.append(candidate)
                    scores.append(sorted_score[i][1])
                    #return candidate,sorted_score[i][1]
        if len(candidates) >= 1:
            N_TOP_RETURN = min(len(candidates),N_TOP_RETURN)
            return candidates[:N_TOP_RETURN],scores[:N_TOP_RETURN]
        for i in xrange(VALID_SIZE):
            if sorted_score[i][1] > config.MIN_CAND_SCORE:
                candidate = sorted_score[i][0]
                candidates.append(candidate)
                scores.append(sorted_score[i][1])
        N_TOP_RETURN = min(len(candidates),N_TOP_RETURN)

        if N_TOP_RETURN > 0:
            return candidates[:N_TOP_RETURN], scores[:N_TOP_RETURN]

        return [wrong_bigram],[0]

    def __fix_wrong_multi_candidates_abb(self, wrong_bigram, true_vocab_priority=True):

        d_candidates = {}
        n_cal = Accumulator()

        def __update_candidates(sub_dict,skip_d = ""):
            if sub_dict == 0 or len(sub_dict) == 0:
                return 0
            n_val = 0
            for candidate, counter in sub_dict.iteritems():
                #print candidate
                #if candidate == u"thu nghiem":
                #    print "Here"
                abb = utils.get_abbv_bigram(candidate)
                if abb == skip_d:
                    continue
                if not self.__is_suitable_length(wrong_bigram, candidate):
                    continue
                try:
                    d_candidates[candidate]
                except:
                    sim_score = cal_sim_score(wrong_bigram, candidate, counter)
                    n_cal.add(1)
                    if sim_score < 0.7:
                        continue
                    if sim_score > 1.0:
                        n_val += 1
                    d_candidates[candidate] = cal_sim_score(wrong_bigram, candidate, counter)
                    if n_val > N_CUTOFF_VALID:
                        break
            return n_val

        abb = utils.get_abbv_bigram(wrong_bigram)
        abb_d = utils.get_zero_dict(self.language_model.abbv_vocab_dict,abb)

        n_val = __update_candidates(abb_d)
        if n_val <= 0:
            c = wrong_bigram[0]

            if c == " ":
                return [wrong_bigram], [0]
            try:

                sub_dict = self.language_model.hierachical_first_char_dict[c]
                __update_candidates(sub_dict,abb)

            except:
                return [wrong_bigram], [0]

        if len(d_candidates) == 0:
            return [wrong_bigram], [0]
        sorted_score = utils.sort_dict(d_candidates)

        print wrong_bigram, sorted_score[:3], len(sorted_score), n_cal.get()

        VALID_SIZE = min(len(sorted_score), N_TOP_CANDIDATES)
        N_TOP_RETURN = G_N_TOP_RETURN
        candidates = []
        scores = []
        if true_vocab_priority:
            for i in xrange(VALID_SIZE):
                candidate = sorted_score[i][0]
                if self.language_model.check_true_bi_bare_vocab(candidate):
                    candidates.append(candidate)
                    scores.append(sorted_score[i][1])
                    # return candidate,sorted_score[i][1]
        if len(candidates) >= 1:
            N_TOP_RETURN = min(len(candidates), N_TOP_RETURN)
            return candidates[:N_TOP_RETURN], scores[:N_TOP_RETURN]
        for i in xrange(VALID_SIZE):
            if sorted_score[i][1] > config.MIN_CAND_SCORE:
                candidate = sorted_score[i][0]
                candidates.append(candidate)
                scores.append(sorted_score[i][1])
        N_TOP_RETURN = min(len(candidates), N_TOP_RETURN)

        if N_TOP_RETURN > 0:
            return candidates[:N_TOP_RETURN], scores[:N_TOP_RETURN]

        return [wrong_bigram], [0]

    def __fix_rule(self, sen):
        return self.rule_fix.replace(sen)


    def fix(self,sen, skip_digit=True, new_true_vocab=""):
        begin = datetime.now()
        segments,spliters = self.__split_segment_sentence(sen)
        correctors = []
        back_refs = []
        self.acm = Accumulator()
        for segment in segments:
            sen_nomial_vocab = self.__create_sen_nomial_vocab(segment)
            corrector,back_ref = self.__fix_segment(segment,skip_digit, new_true_vocab,sen_nomial_vocab)
            correctors.append(corrector)
            back_refs.append(back_ref)
        #results_formatter = []
        #backref_formatter = []
        #for i in xrange(len(correctors)):
        #    results_formatter.append("%s%s"%(correctors[i],spliters[i]))
        #    backref_formatter.append("%s%s"%(back_refs[i],spliters[i]))
        self.__get_runtime(begin,mess="Total")
        print "\tSearching candidates time: ",self.acm.get()
        return self.__merge_sements_with_spliter(correctors,spliters),\
               self.__merge_sements_with_spliter(back_refs,spliters)


    def __fix_segment(self,sen, skip_digit=True, new_true_vocab="",sen_nomial_vocab=""):
        if len(sen) <= 3:
            return sen,sen
        return self.__fix_multi_markov(sen, skip_digit=skip_digit, new_true_vocab=new_true_vocab,sen_nomial_vocab=sen_nomial_vocab)


    def __get_runtime(self,start,mess=""):
        current = datetime.now()
        print "\tRuntime %s"%mess,(current-start)
        return current-start

    def __fix_multi_markov(self, sen, skip_digit=True, new_true_vocab="",sen_nomial_vocab=""):

        sen = self.__fix_rule(sen)
        sen = self.__remove_accent_teencode(sen)
        _tokens = self.language_model.split_sentece(sen)
        back_ref = " ".join(_tokens)

        before_tokens = " ".join(_tokens)
        print "Before tokens: ",before_tokens

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)

        #Fixing for wrong words

        for i in xrange(len(tokens)):
            if not self.language_model.check_true_single_bare_vocab(tokens[i], skip_digit, new_true_vocab,sen_nomial_vocab):
                print "Wrong token: ",tokens[i]

                bigram_back = None
                bigram_next = None
                fix_bigram_backs = []
                fix_bigram_nexts = []
                fix_code_backs = []
                fix_code_nexts = []
                if i > 0:
                    bigram_back = "%s %s"%(tokens[i-1],tokens[i])
                if i < len(tokens) -1 :
                    bigram_next = "%s %s"%(tokens[i],tokens[i+1])

                if bigram_back != None:
                    begin = datetime.now()

                    fix_bigram_backs,fix_code_backs  = self.__fix_wrong_multi_candidates_abb(bigram_back,true_vocab_priority=False)
                    rt = self.__get_runtime(begin)
                    self.acm.add(rt)
                if bigram_next != None:
                    begin = datetime.now()
                    fix_bigram_nexts,fix_code_nexts = self.__fix_wrong_multi_candidates_abb(bigram_next,true_vocab_priority=False)
                    rt = self.__get_runtime(begin)
                    self.acm.add(rt)
                print fix_bigram_backs,fix_code_backs
                print fix_bigram_nexts,fix_code_nexts


                reg_list = []
                repl_list = []
                can_list = []

                sub_first_ind = i-1
                if sub_first_ind < 0:
                    sub_first_ind = 0
                sub_last_ind = i + 3
                if sub_last_ind > len(tokens):
                    sub_last_ind = len(tokens)
                sub_sen = " ".join(tokens[sub_first_ind:sub_last_ind])
                #Back replacing
                if len(fix_code_backs) > 0 and fix_code_backs[0] > 0:
                    back_pattern = self.__fix_regex_marker_pattern(bigram_back)
                    for fix_bigram_back in fix_bigram_backs:
                        reg_back = self.__create_bound_pattern(back_pattern)
                        bare_back_rep = reg_back.sub(fix_bigram_back,sub_sen)
                        #reg_back = re.compile(ur'\b%s\b' % bigram_back, re.UNICODE)
                        #bare_back_rep = reg_back.sub(fix_bigram_back, sub_sen)

                        reg_list.append(reg_back)
                        repl_list.append(fix_bigram_back)
                        can_list.append(bare_back_rep)
                        print fix_bigram_back,":->",bare_back_rep
                #print "Fix code nexts",fix_code_nexts
                if len(fix_code_nexts) > 0 and fix_code_nexts[0] > 0:
                    next_pattern = self.__fix_regex_marker_pattern(bigram_next)
                    for fix_bigram_next in fix_bigram_nexts:
                        reg_next = self.__create_bound_pattern(next_pattern)
                        bare_sub_sen_next = reg_next.sub(fix_bigram_next,sub_sen)
                        #reg_next = re.compile(r"\b%s\b" % bigram_next, re.UNICODE)
                        #bare_sub_sen_next = reg_next.sub(fix_bigram_next, sub_sen)
                        reg_list.append(reg_next)
                        repl_list.append(fix_bigram_next)
                        can_list.append(bare_sub_sen_next)

                        print fix_bigram_next,":->",bare_sub_sen_next


                max_idx = -1
                max_markov_score = -100000
                for i in xrange(len(can_list)):
                    markov_score = self.language_model.get_prob_sentence(can_list[i])
                    print can_list[i],markov_score
                    if markov_score > max_markov_score:
                        max_markov_score = markov_score
                        max_idx = i

                if max_idx >=0:
                    bare_raw_sen = reg_list[max_idx].sub(repl_list[max_idx],bare_raw_sen)
        back_ref = self.__check_back_accent(before_tokens,bare_raw_sen)
        print "Back accent ref: ",back_ref
        return bare_raw_sen,back_ref

    def __create_sen_nomial_vocab(self,sen):
        tokens = sen.split(" ")
        sen_nomial_vocab = set()
        for token in tokens:
            if len(token) > 0 and token[0].isupper():
                sen_nomial_vocab.add(token.lower())
        return sen_nomial_vocab

    def __check_back_accent(self,before,after):
        before_tokens = before.split(" ")
        after_tokens = after.split(" ")
        if len(before_tokens) != len(after_tokens):
            return " ".join(after_tokens)
        back_accent_tokens = []
        for i in xrange(len(after_tokens)):
            if utils.accent2bare(before_tokens[i]) == after_tokens[i]:
                back_accent_tokens.append(before_tokens[i])
            else:
                back_accent_tokens.append(after_tokens[i])
        return " ".join(back_accent_tokens)

    def __split_segment_sentence(self,sen):
        mo_segments = SPLITER_TOKENS.finditer(sen)
        segments = []
        spliters = []
        start_index = 0
        for mo in mo_segments:
            segment = sen[start_index:mo.start()]
            spliter = mo.group(0)
            start_index = mo.start() + len(spliter)
            segments.append(segment)
            spliters.append(spliter)
        return segments,spliters

    def __merge_sements_with_spliter(self,segments,spliters):
        #print segments,spliters
        results = []
        for i in xrange(len(segments)):
            spliter = spliters[i]
            if spliter in BEGIN_TOKENS:
                spliter = " "+spliter
            else:
                spliter = spliter + " "
            results.append("%s%s"%(segments[i],spliter))
        return "".join(results)

    def __remove_accent_teencode(self,sen):
        return ACCENT_TEENCODE_REG.sub("",sen)

    def __create_bound_pattern(self,pattern):
        return re.compile(ur"(?<!\S)%s(?=\s|$)" % pattern)

    def __fix_regex_marker_pattern(self,src):
        return R_MARKER_REF.sub(ur"\\\g<MARKER>",src)

class Accumulator():
    def __init__(self):
        self.__acm = ""
    def add(self,obj):
        if self.__acm == "":
            self.__acm = obj
        else:
            self.__acm = self.__acm + obj
    def get(self):
        return self.__acm

class Test():
    def __init__(self):
        self.lm = LanguageModel.load()
    def run(self):
        print len(self.lm.abbv_vocab_dict["tt"])