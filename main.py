# -*- coding: utf-8 -*-

import os
if __name__ == "__main__":
    #from vnbarefixing import load_data
    #load_data.split_news_sentence()
    #exit(-1)
    from vnbarefixing.bigram_fixing import BigramFixing

    if __name__ == "__main__":
        #print "Training..."
        #BigramFixing.train()
        #exit(-1)
        #bigram = BigramFixing()
        #bigram.save()
        bigram = BigramFixing.load()
        sen = u"Cửa hàg có bán đệin thoại  khôg??"
        fixed_sen, back_ref = bigram.fix(sen)
        print sen
        print fixed_sen
        print back_ref
