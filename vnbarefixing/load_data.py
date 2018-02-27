# -*- coding: utf-8 -*-

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


def split_news_sentence():
    fin = open("%s/AllItemInfor.dat"%DATA_DIR, encoding="utf-8")
    sentences = []
    import sys
    sys.path.insert(0, '..')
    from spelling_corrector import SentenceSpliter
    spliter = SentenceSpliter()
    cc = 0
    fout = open("%s/Sentences_Lines.dat"%DATA_DIR,"w",encoding="utf-8")
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
    #from utils import pickle_save
    #pickle_save(sentences,"%s/All_Sentences.dat"%DATA_DIR)
def get_news_sentence_reader():
    return open("%s/Sentences_Lines.dat"%DATA_DIR,encoding="utf-8")

def load_news_data(is_reload=True):
    if is_reload:
        from utils import pickle_load
        return pickle_load("%s/All_Sentences.dat"%DATA_DIR)
    fin = open("/home/nda/Data/Data_NLP/AllItemInfor.dat",encoding="utf-8")
    sentences = []
    import sys
    sys.path.insert(0, '..')
    from spelling_corrector import SentenceSpliter
    spliter = SentenceSpliter()
    cc = 0
    while True:
        doc = fin.readline()
        if doc == "":
            break
        cc += 1
        if cc %100 == 0:
            print "\r%s"%cc,
        doc = doc.strip().split("||")[-2]
        doc = unicodedata.normalize("NFC",doc)
        sens = spliter.split(doc)
        for sen in sens:
            sentences.append(sen)
    fin.close()
    print "\t\t\tLoaded total %s sentences of %s docs"%(len(sentences),cc)
    return sentences

def export_question_answer_sentences():

    import re
    re_ldots = re.compile("\.\.\.", re.UNICODE)
    re_markers = re.compile("[?,;!]")
    re_dotspace = re.compile("\.")

    def norm_paragraph(para):
        para = para.replace("\r","")
        para = para.replace("\n",". ")
        para = re_ldots.sub(".",para)
        para = re_markers.sub(".",para)
        para = re_dotspace.sub(" . ",para)
        return para
    def split_paragraph(para):
        sentences = para.split(" . ")
        return sentences

    def export():
        fin = open("%s/models/data/inp/fpt_mobiles_product_and_qa.dat" % cdir, "r")
        fout = open("%s/fpt_shop_mobile.dat"%cdir,"w",encoding="utf-8")

        while True:
            line = fin.readline()
            if line == "":
                break
            s = json.loads(line.strip())
            try:
                title = s['title']
                qas = s['comments']
                for qa in qas:
                    try:
                        question = qa[0]
                        para = norm_paragraph(question)
                        sentences = split_paragraph(para)
                        for sen in sentences:
                            sen = sen.strip()
                            if len(sen) < 3:
                                continue

                            fout.write(u"%s\n"%sen)
                    except:
                        pass
                    try:
                        answer = qa[1]
                        para = norm_paragraph(answer)
                        sentences = split_paragraph(para)
                        for sen in sentences:
                            sen = sen.strip()
                            if len(sen)<3:
                                continue
                            fout.write(u"%s\n"%sen)
                    except:
                        pass


            except Exception as e:
                continue

        fin.close()
        fout.close()
    export()
def load_questions():

    fin = open("%s/models/data/inp/fpt_mobiles_product_and_qa.dat"%cdir, "r")
    questions = []
    while True:
        line = fin.readline()
        if line == "":
            break
        s = json.loads(line.strip())
        try:
            title = s['title']
            qas = s['comments']
            for qa in qas:
                questions.append(qa[0])


        except Exception as e:
            continue
    fin.close()
    return questions
def load_question_from_file(path):
    fin = open(path, "r")
    questions = []
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        questions.append(line)
    fin.close()
    return questions


def load_questions2():
    fin = open("%s/models/data/inp/fpt_mobiles_product_and_qa.dat"%cdir, "r")
    questions = []
    while True:
        line = fin.readline()
        if line == "":
            break
        s = json.loads(line.strip())
        try:
            title = s['title']
            qas = s['comments']
            for qa in qas:
                questions.append(qa[0])
            if qa[0].__contains__(u"â"):
                print "XXXXXXXXXXX"


        except Exception as e:
            continue
    fin.close()
    return questions




def load_products():
    fin = open("%s/models/data/inp/fpt_mobiles_product_and_qa.dat"%cdir,"r")
    fout = open("qa","w",encoding="utf-8")
    while True:
        line = fin.readline()
        if line == "":
            break
        s = json.loads(line.strip())
        try:
            title = s['title']
            qas = s['comments']
            fout.write(u"%s\n#QA:\n\n"%title)
            for qa in qas:
                fout.write(u"Q:%s\n"%qa[0])
                fout.write(u"A:%s\n\n"%qa[1])

            fout.write(u"\t============================================\n")

        except Exception as e:
            continue
    fin.close()
    fout.close()
    print "Done"

if __name__=="__main__":
    #load_questions2()
    export_question_answer_sentences()