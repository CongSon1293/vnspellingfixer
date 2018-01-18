# -*- coding: utf-8 -*-

import json
from io import open
import os
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
    load_questions2()
