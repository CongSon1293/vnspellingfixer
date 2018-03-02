import os
import unicodedata
from io import open
import re
from spelling_corrector.general_bare_corrector.general_rules import GeneralRuleFixer

CDIR = os.path.abspath(os.path.dirname(__file__))

class RulesFixing():
    def __init__(self):
        self.__general_fixer = GeneralRuleFixer()
        self.__uni_rules = {}
        self.__domain_rules = {}
        self.__uni_rules_file = "%s/data/stats/uni_fix.dat" % CDIR
        self.__domain_rules_file = "%s/data/rules/domain_rules"%CDIR
    def __load_uni_rules_fixing(self):
        f = open(self.__uni_rules_file, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            line = unicodedata.normalize("NFKC", line.strip())
            parts = line.split(u"\t")
            reg = re.compile(ur"\b%s\b" % parts[0], re.UNICODE)
            self.__uni_rules[reg] = parts[1]

        f.close()
    def __load_domain_rules_fixing(self):

        fin = open(self.__domain_rules_file, "r")
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
                reg_source = re.compile(ur"%s" % source, re.UNICODE)
                self.__domain_rules[reg_source] = repl

            else:
                reg_source = re.compile(ur"\b%s\b" % source, re.UNICODE)
                self.__domain_rules[reg_source] = repl

            print "\tLoaded a domain rule: %s -> %s" % (source, repl)
        fin.close()

    def init(self,level=0):
        if level == 0:
            return
        if level == 1:
            self.__load_domain_rules_fixing()
            self.__load_uni_rules_fixing()
            return
        if level >= 2:
            return
        return
    def __replace_uni_rules(self, sen):
        for reg,repl in self.__uni_rules.iteritems():
            sen = reg.sub(repl,sen)
        return sen
    def __replace_domain_rules(self,sen):
        for reg,repl in self.__domain_rules.iteritems():
            sen = reg.sub(repl,sen)
        return sen

    def fix(self,sen):
        sen = self.__general_fixer.replace(sen)
        sen = self.__replace_uni_rules(sen)
        return sen
