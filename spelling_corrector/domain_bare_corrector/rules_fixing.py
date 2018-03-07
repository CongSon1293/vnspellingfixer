import os
import unicodedata
from io import open
import re
from spelling_corrector.general_bare_corrector.general_rules import GeneralRuleFixer

CDIR = os.path.abspath(os.path.dirname(__file__))
R_MARKER_REF = re.compile(ur"(?P<MARKER>[\'\^\?\~\*])")

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
            pattern = self.__fix_regex_marker_pattern(parts[0])
            reg = self.__create_bound_pattern(pattern)
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
                source_pattern = self.__fix_regex_marker_pattern(source)
                reg_source = self.__create_bound_pattern(source_pattern)
                self.__domain_rules[reg_source] = repl

            #print "\tLoaded a domain rule: %s -> %s" % (source, repl)
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

    def __create_bound_pattern(self,pattern):
        return re.compile(ur"(?<!\S)%s(?=\s|$)" % pattern)
    def __fix_regex_marker_pattern(self,src):
        return R_MARKER_REF.sub(ur"\\\g<MARKER>",src)

