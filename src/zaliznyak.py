from typing import List, Tuple, Optional
import utils
import clexicon_pb2


def _lemma_features_split(string: str, sep: str) -> Tuple[str, List[str]]:
    """ Splits at the specified separator """
    features = []
    i = 0
    while i != -1:
        i = string.find(sep)
        if i == -1:
            features.append(string)
            break
        first = string[:i]
        features.append(first)
        string = string[i + 1:]
    lemma = features[0]
    features = features[1:]
    return lemma, features


def compile_zaliznyak_giella(path: str,
                             wordform_lexicon: Optional[object] = None,
                             lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:
    '''
    Build a wordform and a lemma lexicon databases out of Zaliznyak-Giella data.
    '''

    source = open(path, 'r', encoding='utf8')
    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.CLexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_pb2.CLexicon()

    while True:
        line = source.readline().strip()
        if not line:
            break

        # to skip entries like "щ+N+Neu+Inan+Pl+Nom#.+SENT	щ."
        # since "щ+N+Neu+Inan+Pl+Nom	щ" is already in
        if "#.+SENT" in line:
            continue
        # skipping long compounds (for now), e.g. шеститысячесемисотсемидесятидвухматчевый
        if line.startswith('шести'):
            continue

        lemma_features, wordform = line.split('\t')

        # if a word contains a clitic, both lemmas and their features are provided
        # though separated by # : clitic_lemma+FEAT#lemma+FEAT+etc.
        if "#" in lemma_features:
            l1, l2 = lemma_features.split('#')
            clitic, clitic_features = _lemma_features_split(l1, "+")
            lemma, features = _lemma_features_split(l2, "+")
        else:
            lemma, features = _lemma_features_split(lemma_features, "+")
            clitic = None
            clitic_features = None

        # use unstressed wordform as key for the lexicon, save stressed ortho as pronunciation
        primary_stress = '́'
        secondary_stress = '̀'
        pron_segments = []
        unstressed = ''
        i = 0
        while i < len(wordform):
            if i == (len(wordform) - 1):
                pron_segments.append(wordform[i])
                unstressed += wordform[i]
                break
            if wordform[i + 1] == primary_stress or wordform[i + 1] == secondary_stress:
                pron_segments.append(wordform[i:i + 2])
                unstressed += wordform[i]
                i += 2
            elif wordform[i] == ' ':
                unstressed += wordform[i]
                i += 1
            else:
                pron_segments.append(wordform[i])
                unstressed += wordform[i]
                i += 1

        # add the unstressed wordform + its features to the wordform lexicon
        wordform_lexicon = utils._build_entry(wordform_lexicon, key='wordform', add_wordform=unstressed,
                                              add_lemma=lemma, source='zaliznyak-giella',
                                              morph_features=features,
                                              add_clitic=clitic, add_clitic_features=clitic_features,
                                              add_segments=pron_segments)

        # add the lemma and its features to a separate lemma lexicon
        is_lemma = 0
        if lemma == unstressed:
            if 'V' in features:
                if 'Inf' in features:
                    is_lemma = 1
            elif 'N' in features or 'Pron' in features:
                if 'Nom' in features and 'Sg' in features:
                    is_lemma = 1
            elif 'A' in features or 'Ord' in features or 'Det' in features:
                if 'Nom' in features and 'Sg' in features and 'Msc' in features:
                    is_lemma = 1
            elif 'Num' in features:
                if 'Nom' in features:
                    is_lemma = 1
            else:
                is_lemma = 1
        if is_lemma:
            lemma_lexicon = utils._build_entry(lemma_lexicon, key='lemma', add_lemma=lemma,
                                               source='zaliznyak-giella',
                                               morph_features=features, add_clitic=clitic,
                                               add_clitic_features=clitic_features,
                                               add_segments=pron_segments)
    source.close()
    return wordform_lexicon, lemma_lexicon
