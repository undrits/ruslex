import utils
from typing import Optional, Tuple
import clexicon_v01_pb2


def compile_unimorph(path: str,
                     wordform_lexicon: Optional[object] = None,
                     lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:
    '''
    Build a lemma and a wordform lexicons
    '''

    if not wordform_lexicon:
        wordform_lexicon = clexicon_v01_pb2.CLexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_v01_pb2.CLexicon()

    with open(path, 'r') as source:

        while True:
            line = source.readline().strip()
            if line.startswith("name"):
                continue
            if not line:
                break

            wordform, lemma, features = line.split(',')
            features = features.split(';')

            wordform_lexicon = utils._build_entry(wordform_lexicon, key='wordform',
                                                  add_wordform=wordform, add_lemma=lemma,
                                                  source='unimorph',  morph_features=features)

            is_lemma = 0
            if lemma == wordform:
                if 'V' in features:
                    if 'NFIN' in features:
                        is_lemma = 1
                elif 'N' in features:
                    if 'NOM' in features and 'SG' in features:
                        is_lemma = 1
                elif 'ADJ' in features:
                    if 'NOM' in features and 'SG' in features and 'MASC' in features:
                        is_lemma = 1
                else:
                    is_lemma = 1
            if is_lemma:
                lemma_lexicon = utils._build_entry(lemma_lexicon, key='lemma', add_lemma=lemma,
                                                   source='unimorph', morph_features=features)

    return wordform_lexicon, lemma_lexicon
