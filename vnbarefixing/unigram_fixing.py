# -*- coding: utf-8 -*-
import utils
import vnnorm_stats_unibi
from custom_regex import HardRegex,OneFixRegex,MultiFixRegex,CommonRegex
from io import open

class UnigramFixing():
    def __init__(self):
        vn_vocab = vnnorm_stats_unibi.load_vn_vocab()
        # fixing_map = vnnorm_stats.load_hard_fixing()
        self.hard_regex = HardRegex()
        self.hard_regex.load_from_file()

        self.one_fix = OneFixRegex()
        self.one_fix.load_from_file()

        self.multi_fix = MultiFixRegex()
        self.multi_fix.load_from_file()

        self.common_fixing = CommonRegex()
        self.common_fixing.load_from_file()
    def fix(self,sen,is_lower=True):
        qs = sen
        if not is_lower:
            qs = unicode(qs)
            qs = qs.lower()
        qs = self.hard_regex.replace(qs)
        qs = self.common_fixing.replace(qs)
        qs = self.one_fix.replace(qs)

        return qs



def vn_fix():
    vn_vocab = vnnorm_stats_unibi.load_vn_vocab()
    #fixing_map = vnnorm_stats.load_hard_fixing()
    hard_regex = HardRegex()
    hard_regex.load_from_file()
    one_fix = OneFixRegex()
    one_fix.load_from_file()
    multi_fix = MultiFixRegex()
    multi_fix.load_from_file()

    common_fixing = CommonRegex()
    common_fixing.load_from_file()


    from load_data import load_questions
    questions = load_questions()
    f_fix = open("q_fixing", "w", encoding="utf-8")
    question_norm1 = []
    for qs in questions:
        s = qs
        qs = unicode(qs)
        qs = qs.lower()
        qs = hard_regex.replace(qs)

        qs = common_fixing.replace(qs)
        qs = one_fix.replace(qs)
        qs = multi_fix.replace(qs)
        question_norm1.append(qs)
        f_fix.write(u"%s | %s\n" % (qs,s))
        #print s
        #print qs
        #exit(-1)
    f_fix.close()

if __name__ == "__main__":
    vn_fix()
