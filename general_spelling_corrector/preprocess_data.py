
import json
import os
import unicodedata
from io import open

cdir = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = "/home/nda/Data/Data_NLP"
DATA_SOURCE = "/home/nda/Data/Text/Articles"
NEWS_SENTENCES_DATA = "Sentences_Lines.dat"
SUBTITLES_DATA_SOURCCE = "sub_film.txt"
SUBTITLES_EXPORT_DATA = "norm_sub_film.dat"

def export_subtitles():
    fin = open("%s/%s"%(DATA_SOURCE,SUBTITLES_DATA_SOURCCE),"r")
    fout = open("%s/%s"%(DATA_DIR,SUBTITLES_EXPORT_DATA),"w")
    while True:
        line = fin.readline()
        if line == "":
            break
        line = unicodedata.normalize("NFC", line)
        fout.write(u"%s"%line)
    fin.close()
    fout.close()



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

if __name__ == "__main__":
    #export_subtitles()
    #split_news_sentence()
    pass