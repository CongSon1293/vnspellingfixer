from spelling_corrector.general_bare_corrector.corrector import GeneralBareCorrector
from rules_fixing import RulesFixing
from vocabulary import DomainVocaburaly


class DomainBareCorrector():
    def __init__(self):
        self.domain_vocab = DomainVocaburaly()
        self.domain_vocab.init()
        self.domain_true_bare_vocab = self.domain_vocab.true_bare_univocab
        self.general_corrector = GeneralBareCorrector()
        self.hard_one_rule_fixer = RulesFixing()
        self.hard_one_rule_fixer.init(level=1)

    def fix(self,sen):
        sen = self.hard_one_rule_fixer.fix(sen)
        sen = self.general_corrector.fix_general_bigram(sen,new_true_vocab=self.domain_true_bare_vocab)
        return sen
