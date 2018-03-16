# -*- coding: utf-8 -*-

from stats import WrongUnigramStats,WRONG_UNIGRAM_STATS_FILE
import os
cdir = os.path.abspath(os.path.dirname(__file__))

def run_first_wrong_unigram_stats():
    wrong_unigram_stats = WrongUnigramStats()
    wrong_unigram_stats.export_wrong_words()
    print "Please check the following wrong words. If there is any true token, please add them to data/inp/speacial_tokens"
    os.system("gedit %s/%s"%(cdir,WRONG_UNIGRAM_STATS_FILE))
def run_second_rule_unigram_matching():
    from stats import StatsOneRuleUnigram
    one_rule_stats = StatsOneRuleUnigram()
    one_rule_stats.fix_wrong_words_heuristic()
def run_third_stats_bare_bigram():
    from stats import BareBigramStats
    bare_bigram_stats = BareBigramStats()
    bare_bigram_stats.export_bare_bigram_stats()
def run_fourth_stats_bare_bigram_fixing():
    from stats import BareBigramStats
    bare_bigram_stats = BareBigramStats()
    bare_bigram_stats.stats_bigram_hardfixing()
if __name__ == "__main__":
    #run_first_wrong_unigram_stats()
    #run_second_rule_unigram_matching()
    #run_third_stats_bare_bigram()
    #run_fourth_stats_bare_bigram_fixing()
    pass