# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import os
class MultiFixRegex():
    def __init__(self):
        self.regex = []
        self.sub = []
    def load_from_file(self,path="models/data/out/multi_fix.dat"):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        f = open("%s/%s" % (dir_path, path), "r", encoding="utf-8")
        while True:
            line = f.readline()
            if line == "":
                break
            if line[0] == "#":
                continue
            line = unicodedata.normalize("NFC", line.strip())
            parts = line.split("\t")
            if parts[0] == u"F":
                wrong_word = parts[1]
                fix_word = parts[2]
                next_contexts = parts[3].split(" ")
                for nc in next_contexts:
                    self.regex.append(re.compile(ur"\b%s %s\b"%(wrong_word,nc),re.UNICODE))
                    self.sub.append(u"%s %s"%(fix_word,nc))
            elif parts[0] == u"B":
                wrong_word = parts[1]
                fix_word = parts[2]
                back_contexts = parts[3].split(" ")
                for bc in back_contexts:
                    self.regex.append(re.compile(ur"\b%s %s\b" % (bc, wrong_word), re.UNICODE))
                    self.sub.append(u"%s %s" % (bc, fix_word))

        f.close()

    def replace(self, sen):
        q = sen
        for i in xrange(len(self.regex)):
            reg = self.regex[i]
            sub = self.sub[i]
            q = reg.sub(sub,q)
        return q
class CommonRegex():
    def __init__(self):
        self.s_regex = dict()
    def load_from_file(self,path="models/data/inp/common_fixing"):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:

            f = open("%s/%s" % (dir_path, path), "r", encoding="utf-8")
            while True:
                line = f.readline()
                if line == "":
                    break
                if line[0] == "#":
                    continue
                line = unicodedata.normalize("NFC", line.strip())
                parts = line.split(u"\t")
                reg = re.compile(ur"\b%s\b" % parts[0], re.UNICODE)
                # print parts[0],"---",parts[1]
                self.s_regex[reg] = u"%s"%parts[1]
            f.close()
        except:
            print "An error occurred while loadinng common fixing from %s"%path
            pass

    def replace(self, sen):
        q = sen
        for reg, des in self.s_regex.iteritems():
            q = reg.sub(des, q)
        return q

class OneFixRegex():
    def __init__(self):
        self.s_regex = dict()
    def load_from_file(self,path="models/data/out/one_fix.dat"):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        f = open("%s/%s" % (dir_path, path), "r", encoding="utf-8")
        while True:
            line = f.readline()
            if line == "":
                break
            if line[0] == "#":
                continue
            line = unicodedata.normalize("NFC", line.strip())
            parts = line.split(u"\t")
            reg = re.compile(ur"\b%s\b" % parts[0], re.UNICODE)
            # print parts[0],"---",parts[1]
            self.s_regex[reg] = parts[1]
        f.close()

    def replace(self, sen):
        q = sen
        for reg, des in self.s_regex.iteritems():
            q = reg.sub(des, q)
        return q


class HardRegex():
    def __init__(self):
        self.d_regex = dict()

        pass
    def load_from_file(self,path="models/data/inp/hard_regexes"):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        f = open("%s/%s"%(dir_path,path),"r",encoding="utf-8")
        while True:
            line = f.readline()
            if line == "":
                break
            if line[0] == "#":
                continue
            line = unicodedata.normalize("NFC",line.strip())
            parts = line.split("\t")
            reg = re.compile(ur"\b%s\b"%parts[0],re.UNICODE)
            #print parts[0],"---",parts[1]
            self.d_regex[reg] = parts[1]
        f.close()

    def replace(self,sen):
        q = sen
        for reg,des in self.d_regex.iteritems():
            q = reg.sub(des,q)
        return q


if __name__ == "__main__":
    #print os.getcwd()
    s = u"Chi mình hỏi dịch vụ giao hàng tận nơi có kèm phí ship ko ạ??"
    com = CommonRegex()
    #com.load_from_file()
    reg = re.compile(r"\bng\b",re.UNICODE)

    print s
    s = reg.sub(u"người",s)
    s = com.replace(s)
    print s