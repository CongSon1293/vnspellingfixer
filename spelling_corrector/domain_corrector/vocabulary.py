from io import open
import os
import unicodedata

SPECIAL_TOKENS_FILE = "data/inp/special_tokens"
SPECIAL_WORDS_FILE = "data/inp/special_words"
FULL_VOCABULARY_FILE = "../resources/vocab/full_vocaburaly.txt"
MISSING_VOCAB_FILE = "../resources/vocab/missing_vocab"
CDIR = os.path.abspath(os.path.dirname(__file__))

class DomainVocaburaly():
    def __init__(self):
        self.true_univocab = set()
    def init(self,domain_dir=CDIR):
        self.__load_true_univocab(domain_dir)
    def __load_true_univocab(self,root="."):
        #Loading from the true vocab file
        f = open("%s/%s" % (CDIR,FULL_VOCABULARY_FILE), "r")
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.strip().lower()
            words = line.split(" ")
            for word in words:
                word = unicodedata.normalize('NFC', word)
                self.true_univocab.add(word)
        f.close()

        #Loading missing unigram

        f = open("%s/%s" % (CDIR,MISSING_VOCAB_FILE), "r")
        while True:
            line = f.readline()
            if line == "":
                break
            word = unicodedata.normalize("NFC", line.strip())
            self.true_univocab.add(word)
        f.close()

        #Loading special tokens in the domain

        if root == ".":
            root = CDIR

        f = open("%s/%s" % (root,SPECIAL_TOKENS_FILE), "r")
        while True:
            line = f.readline()
            if line == "":
                break
            word = unicodedata.normalize("NFC", line.strip())
            self.true_univocab.add(word)
        f.close()
