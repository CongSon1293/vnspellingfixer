# -*- coding: utf-8 -*-

from stats import WrongUnigramStats,WRONG_UNIGRAM_STATS_FILE
import os
cdir = os.path.abspath(os.path.dirname(__file__))

def run_first_wrong_unigram_stats():
    wrong_unigram_stats = WrongUnigramStats()
    wrong_unigram_stats.export_wrong_words()
    print "Please check the following wrong words. If there is any true token, please add them to data/inp/speacial_tokens"
    os.system("gedit %s/%s"%(cdir,WRONG_UNIGRAM_STATS_FILE))

if __name__ == "__main__":
    #run_first_wrong_unigram_stats()
    import re
    s = u"tôi co' xxx"
    r = re.compile(ur'(\bco\b)\'', re.UNICODE)
    x = r.sub(u'có', s)
    print x
    print s