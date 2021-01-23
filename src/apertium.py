from typing import Optional, Tuple
import utils
import clexicon_pb2


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def compile_apertium(path: str,
                     wordform_lexicon: Optional[object] = None,
                     lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:

    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.CLexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_pb2.CLexicon()
    with open(path, 'r') as source:
        while True:
            line = source.readline().strip()
            if not line:
                break
            if "REGEXP" in line or " " in line or "-" in line or "#" in line or "~" in line:
                continue
            if line.startswith('>'):
                continue
            if '>:' in line or ':<' in line or ':>' in line or '<:' in line:
                continue
            wordform, lemma_features = line.split(':')
            illicit_symbols = 0
            for i in range(len(wordform)):
                if wordform[i] not in alphabet:
                    illicit_symbols = 1
                    break
            if illicit_symbols:
                continue
            i = lemma_features.find('<')
            lemma = lemma_features[:i]
            features = []
            splits = lemma_features[i + 1:].split('><')
            for split in splits:
                if split.startswith('<'):
                    features.append(split[1:])
                elif split.endswith('>'):
                    features.append(split[:-1])
                else:
                    features.append(split)

            wordform_lexicon = utils._build_entry(wordform_lexicon, key='wordform',
                                                  add_wordform=wordform, add_lemma=lemma,
                                                  source='apertium',  morph_features=features)

            is_lemma = 0
            if lemma == wordform:
                if 'vblex' in features:
                    if 'inf' in features:
                        is_lemma = 1
                elif 'n' in features or 'prn' in features or 'np' in features:
                    if 'nom' in features and 'sg' in features:
                        is_lemma = 1
                elif 'adj' in features or 'num' in features:
                    if 'nom' in features and 'sg' in features and 'm' in features:
                        is_lemma = 1
                else:
                    is_lemma = 1
            if is_lemma:
                lemma_lexicon = utils._build_entry(lemma_lexicon, key='lemma',
                                                   add_lemma=lemma, source='apertium',
                                                   morph_features=features)

    return wordform_lexicon, lemma_lexicon
