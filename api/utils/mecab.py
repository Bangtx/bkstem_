import MeCab
import jaconv


def halfwidth_to_fullwidth(
    source: str, kana: bool = True, ascii: bool = False, digit: bool = False
):
    """
    Convert text from half-width (hankaku) to full-width (zenkaku)
    Ex: 'ﾃｨﾛ･ﾌｨﾅｰﾚ' -> 'ティロ・フィナーレ'
    :param source: text need converting
    :param kana: allow convert japanese characters, default is True
    :param ascii: allow convert alphabet characters, default is False
    :param digit: allow convert numeric characters, default is False
    :return: string
    """
    return jaconv.h2z(source, kana=kana, ascii=ascii, digit=digit)


def fullwidth_to_halfwidth(
    source: str, kana: bool = False, ascii: bool = True, digit: bool = True
):
    """
    Convert text from full-width (zenkaku) to half-width (hankaku)
    Ex: 'ａｂｃ１２３' -> 'abc123'
    :param source: text need converting
    :param kana: allow convert japanese characters, default is False
    :param ascii: allow convert alphabet characters, default is True
    :param digit: allow convert numeric characters, default is True
    :return: string
    """
    return jaconv.z2h(source, kana=kana, ascii=ascii, digit=digit)


def hiragana_to_katakana(source: str):
    """
    Convert from hiragana to katakana
    Ex: 'ともえまみ' -> 'トモエマミ'
    :param source: text need converting
    :return: string
    """
    return jaconv.hira2kata(source)


def katakana_to_hiragana(source: str):
    """
    Convert from katakana to hiragana
    Ex: '巴マミ' -> '巴まみ'
    :param source:
    :return:
    """
    return jaconv.kata2hira(source)


def normalize_text(source: str):
    """
    Normalize text
    - Convert all of japanese character to full-width
    - Convert all of alphanumeric character to half-width
    - normalize character with NFKC form and some japanese character " ' - ー
    :param source: text need converting
    :return: string
    """
    result = jaconv.normalize(source, "NFKC")
    result = halfwidth_to_fullwidth(result)
    result = fullwidth_to_halfwidth(result)
    return result


def get_pronunciation(source: str):
    """
    Get pronunciation (katakana)
    Ex: '今日はよく寝ました' -> 'キョーワヨクネマシタ'
    :param source: source text
    :return: string
    """
    # specify an empty mecabrc
    mecab = MeCab.Tagger("-r/dev/null")

    # Words will be separated by line
    parsed_results = mecab.parse(source).splitlines()
    # The last line is EOS character, just remove it
    parsed_results = parsed_results[:-1]

    result = ""
    for parsed_word in parsed_results:
        # Mecab will separate parts by tab
        if "\t" not in parsed_word:
            continue

        surface_form = parsed_word.split("\t")[0]  # Get surface form
        pronunciation = parsed_word.split("\t")[1]

        # if can't get pronunciation then keep original source
        if pronunciation == "":
            pronunciation = surface_form
        result += pronunciation

    # convert katakana to hiragana
    result = katakana_to_hiragana(result)
    return normalize_text(result)
