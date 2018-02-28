Method:
0. Use hard rules to replace some common errors
1. Normalize to bare format (No accent)
2. Build true vocaburaly from a pre-vocabulary dataset
3. Build bi-gram context from news dataset
4. Build exceptional words (With context if possible)
Fixing:
5. Search out-of-vocab words as wrong word candidates.
    Step 1: No exceptional words
    Step 2: With exceptional words
6. With step size: +-1
    Bigram context with a high priority on true-two-word-vocabulary, then bigram context
    Test for the context of +-2 if existing true-two-word

Todo:
Solve the confict of two possible replacements between backward and forward