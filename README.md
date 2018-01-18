# Usage of vnbarefixing

## Fixing
```
from vnbarefixing.bigram_fixing import BigramFixing
bigram_fixing = BigramFixing.load()
sen = "Sentence tobe fixed"
fixed_bare_sen,ref_accent_sen = bigram_fixing.fix(sen)
```

## Data

Dir: models/data

 * full_vocabulary.txt: Vocaburaly file
 
Dir: models/data/inp

 * common_fixing: contains common fixing with the syntax of each line:
 ```
    (wrong word)\t(true word)
```
 * hard_regexes: contains hard regexes for replacing: 
 ```
     (pattern)\t(sub)
 ```
 * missing_vocab: contains missing words of the vocabulary
 * special_tokens: contains special single token
 * speical_words: contains special words
 
## Training:
 ```
from vnbarefixing.bigram_fixing import BigramFixing
BigramFixing.train(data="",path="")
#data is a list of unicode sentences
#path specifies the file saving sentences
#only select one of them
```