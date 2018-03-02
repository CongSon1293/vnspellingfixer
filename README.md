# Usage of spelling_corrector.general_bare_corrector

## Fixing
###General corrector
```
from spelling_corrector.general_bare_corrector.corrector import GeneralBareCorrector
general_corrector = GeneralBareCorrectord()
inp = "Sentence tobe fixed"
fix,back_ref = corrector.fix_general_bigram(inp)
```
###Domain corrector
```
from spelling_corrector.domain_corrector.corrector import DomainCorrector
domain_corrector = DomainCorrector()
inp = "Sentence tobe fixed"
domain_corrector.fix(inp)

```

## Data input
###General corrector

Dir: spelling_corrector/general_bare_corrector/models/data/inp/

 * extended_bivocab.dat: Extended new bivocab 
 * hard_replaced_rules: Hard rules to replace mistakes. The syntax of each line:
 ```
  (wrong regex)\t(true replacement)
```
###Domain corrector
Dir: spelling_corrector/domain_corrector/data/inp
 * special_tokens: Special tokens of the domain
 * special_words: Special words of the domain
Dir: spelling_corrector/domain_corrector/data/rules
 * domain_rules: similar to hard_replace_rules