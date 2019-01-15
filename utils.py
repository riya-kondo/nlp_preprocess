import MeCab


dic_path = "path/to/dic"
mecab_dic = "mecabrc -d " + dic_path
tagger = MeCab.Tagger(mecab_dic)


def _split_to_words(text, parts, to_stem=False):
    """
    入力: 'これから始まる私の伝説'
    出力: tuple(['これから', '始まる', '私', 'の', '伝説'])
    """
    mecab_result = tagger.parse(text)
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


def words(text, parts=[]):
    '''
    text: 形態素解析をする文(文書の場合等はfor文で呼び出す)
    parts: 抜き出す品詞
    to_stem: 単語をそのまま入れるか,語幹に変換するか
    '''
    words = _split_to_words(text=text, parts=parts, to_stem=False)
    return words


def stems(text, parts=[]):
    stems = _split_to_words(text=text, parts=parts, to_stem=True)
    return stems


if __name__ == '__main__':
    doc = "これから始まる私の伝説"
    doc = words(doc, parts=["動詞"])
    print(doc)
