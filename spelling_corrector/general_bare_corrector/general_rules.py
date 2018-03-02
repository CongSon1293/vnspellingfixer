# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import os

CDIR = os.path.abspath(os.path.dirname(__file__))


class GeneralRuleFixer():
    def __init__(self):
        self.rules = {}
        self.j_rules = {}
        self.__load_rules_from_file()
        self.j_regex = re.compile(ur"(?P<BF>\w)j",re.UNICODE)
    def __load_rules_from_file(self,path="models/data/inp/rules/hard_replaced_rules"):
        full_path = "%s/%s"%(CDIR,path)
        fin = open(full_path,"r")
        while True:
            line = fin.readline()
            if line == "":
                break
            if line.startswith("#"):
                continue
            line = line.strip()
            parts = line.split("\t")
            source = parts[0]
            repl = parts[1]
            if source.startswith("R"):
                source = source[1:]
                reg_source = re.compile(ur"%s"%source,re.UNICODE)
                self.rules[reg_source] = repl

            else:
                reg_source = re.compile(ur"\b%s\b"%source,re.UNICODE)

                if source.__contains__("j"):
                    self.j_rules[reg_source] = repl
                else:
                    self.rules[reg_source] = repl

            print "\tLoaded a new rule: %s -> %s"%(source,repl)
        fin.close()

    def replace_j_rule(self,sen):
        result = sen
        if result.__contains__("j"):
            for reg, repl in self.j_rules.iteritems():
                result = reg.sub(repl, result)
        return result

    def replace_j_regex(self,sen):
        return self.j_regex.sub(ur"\g<BF>i", sen)


    def replace(self,sen):
        result = sen
        result = self.replace_j_rule(result)
        result = self.replace_j_regex(result)
        for reg,repl in self.rules.iteritems():
            result = reg.sub(repl,result)
        return result
if __name__ == "__main__":
    replacer = GeneralRuleFixer()
    sen = "muon gjaj thjch di"
    qq = replacer.replace_j_regex(sen)
    print qq