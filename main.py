# -*- coding: utf-8 -*-

def loop(bigram_model):
    while True:
        s = raw_input("Input: ")
        if len(s) > 4:
            fixed_sen, back_ref = bigram_model.fix(s)
            print s
            print fixed_sen
def old_fix():
    from vnbarefixing.bigram_fixing import BigramFixing

    #print "Training..."
    #BigramFixing.train()
    #exit(-1)
    #bigram = BigramFixing()
    #bigram.save()
    bigram = BigramFixing.load()
    loop(bigram)

def general_fix(pre_vocab = True,loop=True):

    if not pre_vocab:
        from spelling_corrector.general_bare_corrector.vocabulary import Vocaburaly
        vocab = Vocaburaly()
        vocab.init()
        vocab.save()
    if loop:
        from spelling_corrector.general_bare_corrector.corrector import GeneralBareCorrector
        corrector = GeneralBareCorrector()
        while True:
            inp = raw_input("Enter: ")
            if len(inp) > 4:
                fix,back_ref = corrector.fix(inp)
                print fix


def domain_fix():
    from spelling_corrector.domain_bare_corrector.corrector import DomainBareCorrector
    domain_corrector = DomainBareCorrector()
    while True:
        inp = raw_input("Enter: ")
        if len(inp) > 4:
            fix, back_ref = domain_corrector.fix(inp)
            print fix


if __name__ == "__main__":
    #general_fix(pre_vocab=True)
    domain_fix()