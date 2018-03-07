import math
import re

import utils
from general_rules import GeneralRuleFixer
from similarity_metrics import cal_sim_score
from language_model import LanguageModel
import config

N_TOP_CANDIDATES = 4
SIZE_VARIANT = 2
G_N_TOP_RETURN = 2
R_MARKER_REF = re.compile(ur"(?P<MARKER>[\`\'\^\?\~\*])")
ACCENT_TEENCODE_REG = re.compile(ur"(?<=\S)[\`\'\^\?\~\*]")
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


        if sorted_score[0][1] > .99:
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
            return [wrong_bigram],[0]
        sorted_score = utils.sort_dict(d_candidates)

        print sorted_score[:3],len(sorted_score)
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
            if sorted_score[i][1] > .99:
                candidate = sorted_score[i][0]
                candidates.append(candidate)
                scores.append(sorted_score[i][1])
        N_TOP_RETURN = min(len(candidates),N_TOP_RETURN)

        if N_TOP_RETURN > 0:
            return candidates[:N_TOP_RETURN], scores[:N_TOP_RETURN]

        return [wrong_bigram],[0]

    def __fix_rule(self, sen):
        return self.rule_fix.replace(sen)
    def fix(self,sen, skip_digit=True, new_true_vocab=""):
        if config.USING_MARKOV == 1:
            return self.__fix_markov(sen, skip_digit=skip_digit, new_true_vocab=new_true_vocab)
        if config.USING_MARKOV == 2:
            return self.__fix_multi_markov(sen, skip_digit=skip_digit, new_true_vocab=new_true_vocab)
        else:
            return self.__fix_bigram(sen, skip_digit=skip_digit, new_true_vocab=new_true_vocab)
    def __fix_bigram(self, sen, skip_digit=True, new_true_vocab=""):


        sen = self.__fix_rule(sen)
        _tokens = self.language_model.split_sentece(sen)
        back_ref = " ".join(_tokens)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)

        #Fixing for wrong words

        for i in xrange(len(tokens)):
            if not self.language_model.check_true_single_bare_vocab(tokens[i], skip_digit, new_true_vocab):
                print "Wrong token: ",tokens[i]

                bigram_back = None
                bigram_next = None
                fix_bigram_back = None
                fix_bigram_next = None
                fix_code_back = 0
                fix_code_next = 0
                if i > 0:
                    bigram_back = "%s %s"%(tokens[i-1],tokens[i])
                if i < len(tokens) -1 :
                    bigram_next = "%s %s"%(tokens[i],tokens[i+1])

                if bigram_back != None:
                    fix_bigram_back,fix_code_back  = self.__fix_wrong_candidate(bigram_back)
                if bigram_next != None:
                    fix_bigram_next,fix_code_next = self.__fix_wrong_candidate(bigram_next)
                print fix_bigram_back,fix_code_back
                print fix_bigram_next,fix_code_next

                if fix_code_back > 0:
                    print "Back",fix_code_next==0
                    if fix_code_next == 0 or self.language_model.check_true_bi_bare_vocab(fix_bigram_back):
                        back_pattern = self.__fix_regex_marker_pattern(bigram_back)
                        reg = self.__create_bound_pattern(back_pattern)
                        bare_raw_sen = reg.sub(fix_bigram_back, bare_raw_sen)
                        print "Replacing...",bigram_back,":",fix_bigram_back,":",bare_raw_sen
                        continue

                if fix_code_next != 0:
                    if fix_code_back < fix_code_next or self.language_model.check_true_bi_bare_vocab(fix_code_next):

                        next_pattern = self.__fix_regex_marker_pattern(bigram_next)
                        reg_next = self.__create_bound_pattern(next_pattern)
                        bare_raw_sen = reg_next.sub(fix_bigram_next, bare_raw_sen)
                    elif fix_code_back > fix_code_next:
                        back_pattern = self.__fix_regex_marker_pattern(bigram_back)
                        reg = self.__create_bound_pattern(back_pattern)
                        bare_raw_sen = reg.sub(fix_bigram_back, bare_raw_sen)
                        continue

        return bare_raw_sen,back_ref


    def __fix_markov(self, sen, skip_digit=True, new_true_vocab=""):

        sen = self.__fix_rule(sen)
        _tokens = self.language_model.split_sentece(sen)
        back_ref = " ".join(_tokens)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)

        #Fixing for wrong words

        for i in xrange(len(tokens)):
            if not self.language_model.check_true_single_bare_vocab(tokens[i], skip_digit, new_true_vocab):
                print "Wrong token: ",tokens[i]

                bigram_back = None
                bigram_next = None
                fix_bigram_back = None
                fix_bigram_next = None
                fix_code_back = 0
                fix_code_next = 0
                if i > 0:
                    bigram_back = "%s %s"%(tokens[i-1],tokens[i])
                if i < len(tokens) -1 :
                    bigram_next = "%s %s"%(tokens[i],tokens[i+1])

                if bigram_back != None:
                    fix_bigram_back,fix_code_back  = self.__fix_wrong_candidate(bigram_back)
                if bigram_next != None:
                    fix_bigram_next,fix_code_next = self.__fix_wrong_candidate(bigram_next)
                print fix_bigram_back,fix_code_back
                print fix_bigram_next,fix_code_next


                if fix_code_back > 0:
                    print "Back with next",fix_code_next!=0
                    if fix_code_next == 0:
                        back_pattern = self.__fix_regex_marker_pattern(bigram_back)
                        #reg = re.compile(ur'\b%s\b' % bigram_back, re.UNICODE)
                        #bare_raw_sen = reg.sub(fix_bigram_back, bare_raw_sen)
                        reg = self.__create_bound_pattern(back_pattern)
                        bare_raw_sen = reg.sub(fix_bigram_back,bare_raw_sen)
                        print "Replacing back only...",bigram_back,":",fix_bigram_back,":",bare_raw_sen
                        continue

                if fix_code_next != 0:
                    if fix_code_back == 0:
                        next_pattern = self.__fix_regex_marker_pattern(bigram_next)
                        #reg = re.compile(r"\b%s\b"%bigram_next,re.UNICODE)
                        #bare_raw_sen = reg.sub(fix_bigram_next,bare_raw_sen)
                        reg = self.__create_bound_pattern(next_pattern)
                        bare_raw_sen = reg.sub(fix_bigram_next,bare_raw_sen)
                        print "Replacing next only...",bigram_next,":",fix_bigram_next
                        continue

                #Stats multi cases:
                if fix_code_back >0 and fix_code_next>0:
                    sub_sen = " ".join(tokens[i-1:i+2])

                    back_pattern = self.__fix_regex_marker_pattern(bigram_back)
                    reg_back = self.__create_bound_pattern(back_pattern)

                    #reg_back = re.compile(ur'\b%s\b' % bigram_back, re.UNICODE)
                    bare_sub_sen_back = reg_back.sub(fix_bigram_back, sub_sen)

                    next_pattern = self.__fix_regex_marker_pattern(bigram_next)
                    reg_next = self.__create_bound_pattern(next_pattern)
                    #reg_next = re.compile(r"\b%s\b" % bigram_next, re.UNICODE)
                    bare_sub_sen_next = reg_next.sub(fix_bigram_next, sub_sen)

                    score_back = self.language_model.get_prob_sentence(bare_sub_sen_back)
                    score_next = self.language_model.get_prob_sentence(bare_sub_sen_next)
                    print score_back,score_next
                    if score_back > score_next:
                        bare_raw_sen = reg_back.sub(fix_bigram_back,bare_raw_sen)
                        continue
                    else:
                        bare_raw_sen = reg_next.sub(fix_bigram_next,bare_raw_sen)
                        continue
        return bare_raw_sen,back_ref


    def __fix_multi_markov(self, sen, skip_digit=True, new_true_vocab=""):

        sen = self.__fix_rule(sen)
        sen = self.__remove_accent_teencode(sen)
        _tokens = self.language_model.split_sentece(sen)
        back_ref = " ".join(_tokens)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)

        #Fixing for wrong words

        for i in xrange(len(tokens)):
            if not self.language_model.check_true_single_bare_vocab(tokens[i], skip_digit, new_true_vocab):
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
                    fix_bigram_backs,fix_code_backs  = self.__fix_wrong_multi_candidates(bigram_back,true_vocab_priority=False)
                if bigram_next != None:
                    fix_bigram_nexts,fix_code_nexts = self.__fix_wrong_multi_candidates(bigram_next,true_vocab_priority=False)
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

        return bare_raw_sen,back_ref


    def __remove_accent_teencode(self,sen):
        return ACCENT_TEENCODE_REG.sub("",sen)


    def __create_bound_pattern(self,pattern):
        return re.compile(ur"(?<!\S)%s(?=\s|$)" % pattern)


    def __fix_regex_marker_pattern(self,src):
        return R_MARKER_REF.sub(ur"\\\g<MARKER>",src)
