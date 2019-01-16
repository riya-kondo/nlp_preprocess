# nlp_preprocess
preprocessing for nlp

# utils.py
you need to install MeCab on your PC.

When you use this module, documents that you want to process should be consisted as list like this.
>[[今日はいい天気],[明日は休みです],[早く帰った方が良い]]

# making_dict.py
How to use.
>import making_dict
>vocab = making_dict.Vocab(sentences)

'sentences' is list, and elements of the list are consisted words list.
>#example
>sentences = [['today', 'is', 'sunny'], ['tomorrow', 'is', 'holiday'], ['you', 'should', 'back', 'home', 'earlier']]

You can specify word's minimum frequency and word's above ratio.
Those are given as 'min_freq' and 'above_ratio'
