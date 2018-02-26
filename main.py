# -*- coding: utf-8 -*-

import os
def train():
    from vnbarefixing.bigram_fixing import BigramFixing
    BigramFixing.train()
    exit(-1)


def loop():
    from vnbarefixing.bigram_fixing import BigramFixing

    bigram = BigramFixing.load()
    while True:
        inp = raw_input("Enter: ")
        if len(inp)>4:
            fixed_sen, back_ref = bigram.fix(inp)
            print fixed_sen
            print back_ref

if __name__ == "__main__":

    loop()