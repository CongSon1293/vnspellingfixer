# -*- coding: utf-8 -*-

import os
if __name__ == "__main__":
    from vnbarefixing.bigram_fixing import BigramFixing

    if __name__ == "__main__":
        #BigramFixing.train()
        bigram = BigramFixing()
        bigram.save()
        bigram = BigramFixing.load()
        sen = u"Điện thoại này có kinh cường lực ko"
        fixed_sen, back_ref = bigram.fix(sen)
        print sen
        print fixed_sen
        print back_ref
