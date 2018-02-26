
import json
import os
import unicodedata
from io import open

cdir = os.path.abspath(os.path.dirname(__file__))

'''
    Product data structure:
    Json:
    {
        title: "Title"
        {key-property: Ram, CPU,Monitor...} : "Value"
        commments: List-Of-Question-Answer-Pairs:[[Q1,A1],[Q2,A2],[Q3,A3],...]
    }
'''
DATA_DIR = "/home/nda/Data/Data_NLP"
NEWS_SENTENCES_DATA = "Sentences_Lines.dat"


def split_news_sentence():
    fin = open("%s/AllItemInfor.dat"%DATA_DIR, encoding="utf-8")
    sentences = []
    import sys
    sys.path.insert(0, '..')
    from vnspliter.sentence_spliter import SentenceSpliter
    spliter = SentenceSpliter()
    cc = 0
    fout = open("%s/%s"%(DATA_DIR,NEWS_SENTENCES_DATA),"w",encoding="utf-8")
    while True:
        doc = fin.readline()
        if doc == "":
            break
        cc += 1
        if cc % 100 == 0:
            print "\r%s" % cc,
        doc = doc.strip().split("||")[-2]
        doc = unicodedata.normalize("NFC", doc)
        sens = spliter.split(doc)
        for sen in sens:
        #    sentences.append(sen)
            fout.write(u"%s\n"%sen)
    fin.close()
    fout.close()
    print "\t\t\tLoaded total %s sentences of %s docs" % (len(sentences), cc)

