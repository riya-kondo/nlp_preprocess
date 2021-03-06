# -*- coding: utf-8 -*-
import argparse
import MeCab
import nltk
from nltk import stem

class splitter():
    def __init__(self, dic_path=''):
        return

    def _split_sentence(self, text, parts, to_stem=False):
        raise NotImplementedError

    def words(self, text, parts=[]):
        '''
        text: 形態素解析をする文(文書の場合等はfor文で呼び出す)
        parts: 抜き出す品詞
        to_stem: 単語をそのまま入れるか,語幹に変換するか
        '''
        words = self._split_sentence(text=text, parts=parts, to_stem=False)
        return words

    def stems(self, text, parts=[]):
        stems = self._split_sentence(text=text, parts=parts, to_stem=True)
        return stems


class ja_splitter(splitter):
    def __init__(self, dic_path=''):
        super(ja_splitter, self).__init__()
        if dic_path:
            self.tagger = MeCab.Tagger('mecabrc -d ' + dic_path)
        else:
            self.tagger = MeCab.Tagger('mecabrc')

    def _split_sentence(self, text, parts, to_stem=False):
        """
        入力: 'これから始まる私の伝説'
        出力: tuple(['これから', '始まる', '私', 'の', '伝説'])
        """
        mecab_result = self.tagger.parse(text)
        info_of_words = mecab_result.split('\n')
        words = []
        for info in info_of_words:
            # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
            if info == 'EOS' or info == '':
                break
                # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
            info_elems = info.split(',')
            # partsに入れた品詞のみ抽出
            if parts:
                if not(info_elems[0].split("\t")[1] in parts):
                    continue
            # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
            if info_elems[6] == '*':
                # info_elems[0] => 'ヴァンロッサム\t名詞'
                words.append(info_elems[0][:-3])
                continue
            if to_stem:
                # 語幹に変換
                words.append(info_elems[6])
                continue

            # 語をそのまま
            words.append(info_elems[0][:-3])
            words = [x.replace("\t", "") for x in words]
        return words


class en_splitter(splitter):
    def __init__(self):
        super(en_splitter, self).__init__()
    
    def _split_sentence(self, text, parts, to_stem=False):
        info_of_words = nltk.word_tokenize(text)
        words = []
        if to_stem:
            stemmer = stem.WordNetLemmatizer()
            for w in info_of_words:
                w = w.lower()
                w = stemmer.lemmatize(w)
                words.append(w)
        else:
            for w in info_of_words:
                w = w.lower()
                words.append(w)
        return words

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="日本語と英語用の事前処理機")
    parser.add_argument('-m', '--mode', default='ja', choices=['ja', 'en'],  help='モード(ja:日本, en:英語)')
    parser.add_argument('--dict', default='',  help='日本語モードで必要。Mecabの辞書。')
    arg = parser.parse_args()
    if arg.mode=='ja':
        spl = ja_splitter(arg.dict)
        text = input("input japanese sentence: ")
    else:
        spl = en_splitter()
        text = input("input english sentence: ")
    
    word_list = spl.words(text)
    stem_list = spl.stems(text)
    print(word_list)
    print(stem_list)
