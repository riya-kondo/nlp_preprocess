# -*- coding: utf-8 -*-
from gensim import corpora
import pickle as p


class Vocab:
    '''
    words: 分かち書きされた文書のリスト
    min_freq: 単語の最低出現頻度(回数)
    above_ratio: 単語の出現回数の割合(多いものを除去)
    prune_at: メモリ制限(無効にするときはNoneを指定)
    self.token: {単語:id}の辞書(idは1~self.vocab)
    self.docs: wordsをid化したリスト
    self.vocab: ボキャブラリー数
    '''
    def __init__(self, words, min_freq=0, above_ratio=1.0, prune_at=2000000):
        dictionary = corpora.Dictionary(words, prune_at=prune_at)
        dictionary.filter_extremes(no_below=min_freq, no_above=above_ratio)
        # id[0]の単語を辞書末尾へ移動(0はパディング用にする)
        token = dictionary.token2id
        ser = [k for k, v in token.items() if v == 0]
        del token[ser[0]]
        token[ser[0]] = len(token)
        self.token = token
        # 文書をID化
        self.docs = self._documents(words)
        self.vocab = len(self.token)

    def _documents(self, words):
        docs = []
        for word in words:
            w = []
            for index in word:
                try:
                    w.append(self.token[index])
                except KeyError:
                    w.append(0)
            docs.append(w)
        return docs

    def id2token(self):
        '''
        self.tokenのkeyとvalueをひっくり返してreturn
        {id:単語}の辞書
        '''
        dic = {}
        for k, v in self.token.items():
            dic[v] = k
        return dic

    def save_obj(self, file_name):
        '''
        dumpを保存(バイナリ形式)
        file_nameはパス指定
        '''
        with open(file_name, 'wb') as f:
            p.dump(self, f)
