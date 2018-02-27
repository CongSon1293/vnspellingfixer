# Usage of spelling_corrector.general_bare_corrector

## Fixing
```
from spelling_corrector.general_bare_corrector.corrector import GeneralBareCorrector
general_corrector = GeneralBareCorrectord()
sen = "Sentence tobe fixed"
fix,back_ref = corrector.fix_general_bigram(inp)
```

## Data input

Dir: spelling_corrector/general_bare_corrector/models/data/inp/

 * extended_bivocab.dat: Extended new bivocab 
 * inp/hard_replaced_rules: Hard rules to replace mistakes. The syntax of each line:
 ```
  (wrong regex)\t(true replacement)
```
