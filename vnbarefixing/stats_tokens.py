from tokenizer.tokenizer import Tokenizer
from load_data import load_questions
from vocabulary import Vocabulary
from io import open
import utils


Q_VOCAB_NAME = "q_vocab.dat"
Q_BARE_VOCAB_NAME = "q_bare_vocab.dat"

question_list = []
def first_stats():
    tokenizer = Tokenizer()
    tokenizer.run()
    question_vocabulary = Vocabulary()

    questions = load_questions()
    cc = 0
    for question in questions:
        #print question
        if cc % 10 == 0:
            print "\r%s"%cc,
        cc += 1
        sen = tokenizer.predict(question)
        sen = sen.lower()
        tokens = question_vocabulary.get_sentence_token_ids(sen)
        question_list.append(tokens)
    print "\n Saving..."
    question_vocabulary.save(Q_VOCAB_NAME)
    utils.pickle_save(question_list,"question_tokens.dat")

    print "Done"
def first_bare_tokens():
    question_bare_vocabulary = Vocabulary()

    f = open("dat/bare_questions.dat","r")

    cc = 0
    while True:
        line = f.readline()
        if line == "":
            break

        # print question
        if cc % 10 == 0:
            print "\r%s" % cc,
        cc += 1
        sen = line.strip()
        tokens = question_bare_vocabulary.get_sentence_token_ids(sen)
        question_list.append(tokens)
    print "\n Saving..."
    f.close()
    question_bare_vocabulary.save(Q_BARE_VOCAB_NAME)
    utils.pickle_save(question_list, "question_bare_tokens.dat")


def stats_bare_tokens():
    vocaburary = Vocabulary.load(Q_BARE_VOCAB_NAME)
    kvs = []
    for key, value in sorted(vocaburary.doc_freq.iteritems(), key=lambda (k, v): (v, k)):
        kvs.append([key, value])

    TOP_TOKEN = set()
    question_list = utils.pickle_load("question_bare_tokens.dat")

    for i in xrange(1, 100):
        key, value = kvs[-i][0], kvs[-i][1]
        # print vocaburary.id_2_token[key],value
        TOP_TOKEN.add(key)

    f_pattern = open("q_bare_pattern.dat", "w", encoding="utf-8")
    for question in question_list:
        pattern = []
        origin = []
        counting = 0
        for token in question:
            if token in TOP_TOKEN:
                s_token = vocaburary.id_2_token[token]
                counting += 1
            else:
                s_token = "*"
            pattern.append(s_token)
            w = vocaburary.id_2_token[token]
            origin.append(w)
        if counting > 0:
            pattern = " ".join(pattern)
            origin = " ".join(origin)
            f_pattern.write(u"%s\t|\t%s\n" % (pattern, origin))
    f_pattern.close()


def stats():
    vocaburary = Vocabulary.load(Q_VOCAB_NAME)
    kvs = []
    for key, value in sorted(vocaburary.doc_freq.iteritems(), key=lambda (k, v): (v, k)):
        kvs.append([key,value])

    TOP_TOKEN = set()
    question_list = utils.pickle_load("question_tokens.dat")


    for i in xrange(1,200):
        key,value = kvs[-i][0],kvs[-i][1]
        #print vocaburary.id_2_token[key],value
        TOP_TOKEN.add(key)

    f_pattern = open("q_pattern.dat","w",encoding="utf-8")
    for question in question_list:
        pattern = []
        origin = []
        counting = 0
        for token in question:
            if token in TOP_TOKEN:
                s_token = vocaburary.id_2_token[token]
                counting += 1
            else:
                s_token = "*"
            pattern.append(s_token)
            w = vocaburary.id_2_token[token]
            origin.append(w)
        if counting > 0:
            pattern = " ".join(pattern)
            origin = " ".join(origin)
            f_pattern.write(u"%s\t|\t%s\n"%(pattern,origin))
    f_pattern.close()
if __name__ == "__main__":
    #first_stats()
    #stats()
    #first_bare_tokens()
    stats_bare_tokens()