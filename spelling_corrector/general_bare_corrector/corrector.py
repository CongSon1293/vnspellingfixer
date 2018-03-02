import math
import re

import utils
from general_rules import GeneralRuleFixer
from similarity_metrics import cal_sim_score
from vocabulary import Vocaburaly

N_TOP_CANDIDATES = 4
SIZE_VARIANT = 2
class GeneralBareCorrector():
    def __init__(self,pre_vocab = True):
        if not pre_vocab:
            self.vocab = Vocaburaly()
            self.vocab.__load_true_vocab()
            self.vocab.__load_all_news_bi_words()
            self.vocab.save()
        else:
            self.vocab = Vocaburaly.load()
            self.vocab.load_extended_true_bivocab()
        self.rule_fix = GeneralRuleFixer()

    def __is_suitable_length(self,word,candidate,size=SIZE_VARIANT):
        if math.fabs(len(word)-len(candidate)) <= SIZE_VARIANT:
            return True
        return False
    def __is_true_biword(self,tokens,current_index,offset):
        start_index = current_index + offset
        if start_index >= 0 and start_index < len(tokens) - 1:
            biword = "%s %s"%(tokens[start_index],tokens[start_index+1])
            return self.vocab.check_true_bi_bare_vocab(biword)
        return False



    def __fix_wrong_candidate(self, wrong_bigram,true_vocab_priority=True):
        d_candidates = {}
        c = wrong_bigram[0]

        if c == " ":
            return wrong_bigram,0
        try:
            sub_dict = self.vocab.hierachical_first_char_dict[c]
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

        print sorted_score
        VALID_SIZE = min(len(sorted_score),N_TOP_CANDIDATES)

        if true_vocab_priority:
            for i in xrange(VALID_SIZE):
                candidate = sorted_score[i][0]
                if self.vocab.check_true_bi_bare_vocab(candidate):
                    return candidate,sorted_score[i][1]


        if sorted_score[0][1] > .99:
            candidate = sorted_score[0][0]
            return candidate,sorted_score[0][1]

        return wrong_bigram,0


    def fix_rule(self,sen):
        return self.rule_fix.replace(sen)

    def fix_general_bigram(self,sen,skip_digit=True,new_true_vocab=""):


        sen = self.fix_rule(sen)
        _tokens = self.vocab.split_sentece(sen)
        back_ref = " ".join(_tokens)

        tokens = []
        for token in _tokens:
            token = utils.accent2bare(token)
            tokens.append(token)

        bare_raw_sen = " ".join(tokens)

        #Fixing for wrong words

        for i in xrange(len(tokens)):
            if not self.vocab.check_true_single_bare_vocab(tokens[i],skip_digit,new_true_vocab):
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
                    if fix_code_next == 0 or self.vocab.check_true_bi_bare_vocab(fix_bigram_back):
                        reg = re.compile(ur'\b%s\b' % bigram_back, re.UNICODE)
                        bare_raw_sen = reg.sub(fix_bigram_back, bare_raw_sen)
                        print "Replacing...",bigram_back,":",fix_bigram_back,":",bare_raw_sen
                        continue

                if fix_code_next != 0:
                    if fix_code_back < fix_code_next or self.vocab.check_true_bi_bare_vocab(fix_code_next):
                        reg = re.compile(r"\b%s\b"%bigram_next,re.UNICODE)
                        bare_raw_sen = reg.sub(fix_bigram_next,bare_raw_sen)
                    elif fix_code_back > fix_code_next:
                        reg = re.compile(r"\b%s\b" % bigram_back, re.UNICODE)
                        bare_raw_sen = reg.sub(fix_bigram_back, bare_raw_sen)
                        continue



        return bare_raw_sen,back_ref

