# -*- coding: utf-8 -*-
import collections
import pickle as p


class Vocab:
    '''
    words: 分かち書きされた文書のリスト
    min_freq: 単語の最低出現頻度(回数)
    above_ratio: 単語の出現回数の割合[0.0~1.0](多いものを除去)
    stop_words: ストップワードのリスト
    stop_words: ストップワードのリスト
    self.vocab: {単語:id}の辞書(idは1~self.vocab_num)
    self.docs: wordsをid化したリスト
    self.vocab_num: 単語数
    '''
    def __init__(self, words, min_freq=0, above_ratio=1.0, stop_words=[]):
        self.vocab, self.vocab_num = self._make_vocab_dic(words, min_freq,
                                                          above_ratio,
                                                          stop_words)
        # 文書をID化
        self.docs = self._documents(words)

    def _make_vocab_dic(self, words, min_freq, above_ratio, stop_words):
        vocab = {}
        all_words = []
        for s in words:
            all_words.extend(s)
        words_counts = collections.Counter(all_words)
        vocab_num = len(words_counts)
        i = 1
        for k, v in words_counts.items():
            if v < min_freq:
                continue
            if (float(v)/vocab_num) > above_ratio:
                continue
            if stop_words:
                if k in stop_words:
                    continue
            vocab[k] = i
            i += 1
        vocab_num = len(vocab)
        return vocab, vocab_num

    def _documents(self, words):
        '''
        文書をself.vocabのIDに変換する。
        min_freqとabove_ratioでフィルタリングした単語は0に置換される
        '''
        docs = []
        for word in words:
            w = []
            for index in word:
                try:
                    w.append(self.vocab[index])
                except KeyError:
                    w.append(0)
            docs.append(w)
        return docs

    def id2word(self):
        '''
        self.vocabのkeyとvalueをひっくり返してreturn
        {id:単語}の辞書
        '''
        dic = {}
        for k, v in self.vocab.items():
            dic[v] = k
        self.id2word = dic
        return dic

    def save_obj(self, file_name):
        '''
        dumpを保存(バイナリ形式)
        file_nameはパス指定
        '''
        with open(file_name, 'wb') as f:
            p.dump(self, f)
