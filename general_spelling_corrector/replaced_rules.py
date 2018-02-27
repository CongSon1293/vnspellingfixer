# -*- coding: utf-8 -*-

import re
import unicodedata
from io import open
import os

CDIR = os.path.abspath(os.path.dirname(__file__))


class ForcingReplace():
    def __init__(self):
        self.rules = {}
        self.__load_rules_from_file()
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
            reg_source = re.compile(ur"\b%s\b"%source,re.UNICODE)
            self.rules[reg_source] = repl
            print "\tLoaded a new rule: %s -> %s"%(source,repl)
        fin.close()

    def replace(self,sen):
        result = sen
        for reg,repl in self.rules.iteritems():
            result = reg.sub(repl,result)
        return result
