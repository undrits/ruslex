from typing import List, Tuple, Optional
import clexicon_pb2


ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'


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


def _build_entry(lexicon: clexicon_pb2.Lexicon,
                 key: str = 'wordform', # or 'lemma'
                 source: str = None,
                 add_wordform: Optional[str] = None,
                 add_lemma: Optional[str] = None,
                 morph_features: Optional[List[str]] = None,
                 add_clitic: Optional[str] = None,
                 add_clitic_features: Optional[List[str]] = None,
                 add_phones: Optional[List[str]] = None,
                 add_segments: Optional[List[str]] = None,
                 add_syllables: Optional[List[str]] = None,
                 ) -> object:

    """ Internal function for building the protobuf lexicon entry """

    # wordform lexicon
    if key == 'wordform':
        entry = lexicon.analyses[add_wordform].analysis.add()
        if add_lemma:
            entry.lemma = add_lemma

    # lemma lexicon
    elif key == 'lemma':
        assert add_lemma, 'No lemma provided for the lemma lexicon'
        entry = lexicon.analyses[add_lemma].analysis.add()

    # indicate source
    assert source, 'The source of the data is not specified'
    entry.source = source

    # adding morphological features
    if morph_features:
        morphology = entry.morphology
        morphology.morph_features.extend(morph_features)
        # if a clitic provided, its lemma and features are also added to the Morphology message
        # only provided in Zaliznyak-Giella data, so added together with morph_features
        # might need to change if clitic info provided without morph_features
        if add_clitic:
            clitics = morphology.clitics.add()
            clitics.clitic = add_clitic
            if add_clitic_features:
                clitics.morph_features.extend(add_clitic_features)

    # adding pronunciation data
    if add_phones or add_segments or add_syllables:
        pronunciation = entry.pronunciation.add()
        if add_phones:
            pronunciation.phone.extend(add_phones)
        if add_segments:
            pronunciation.segment.extend(add_segments)
        # no syllable data so far
        if add_syllables:
            pronunciation.syllable.extend(add_syllables)

    return lexicon


def _compile_apertium(path: str,
                     wordform_lexicon: Optional[object] = None,
                     lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:

    """ Compile a lemma and wordform lexicon out of Apertium data """

    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.Lexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_pb2.Lexicon()
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
                if wordform[i] not in ALPHABET:
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

            wordform_lexicon = _build_entry(wordform_lexicon, key='wordform',
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
                lemma_lexicon = _build_entry(lemma_lexicon, key='lemma',
                                                   add_lemma=lemma, source='apertium',
                                                   morph_features=features)

    return wordform_lexicon, lemma_lexicon


def _compile_unimorph(path: str,
                     wordform_lexicon: Optional[object] = None,
                     lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:

    """ Build a lemma and a wordform lexicons from UniMorph data """

    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.Lexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_pb2.Lexicon()

    with open(path, 'r') as source:

        while True:
            line = source.readline().strip()
            if line.startswith("name"):
                continue
            if not line:
                break

            wordform, lemma, features = line.split(',')
            features = features.split(';')

            wordform_lexicon = _build_entry(wordform_lexicon, key='wordform',
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
                lemma_lexicon = _build_entry(lemma_lexicon, key='lemma', add_lemma=lemma,
                                                   source='unimorph', morph_features=features)

    return wordform_lexicon, lemma_lexicon


def _compile_wikipron(path: str,
                     wordform_lexicon: Optional[object] = None) -> object:

    """ Build a wordform lexicon from WikiPron with pronunciation features """

    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.Lexicon()

    with open(path, 'r') as source:
        while True:
            line = source.readline().strip()
            if not line:
                break

            wordform, transcription = line.split('\t')
            segments = transcription.split(' ')
            phones = []
            i = 0
            while i < len(segments):
                if len(segments) - i == 1:
                    phones.append(segments[i])
                    break
                # phones with palatalization are split into 3 separate phones,
                # e.g. m ⁽ʲ ⁾ (instead of m⁽ʲ⁾ )
                if segments[i + 1].startswith('⁽'):
                    new_phone = segments[i] + segments[i + 1] + segments[i + 2]
                    phones.append(new_phone)
                    i += 3
                else:
                    phones.append(segments[i])
                    i += 1

            # add entry to the lexicon
            wordform_lexicon = _build_entry(wordform_lexicon, key='wordform',
                                                  add_wordform=wordform, source='wikipron',
                                                  add_phones=phones)

    return wordform_lexicon


def _compile_zaliznyak_giella(path: str,
                             wordform_lexicon: Optional[object] = None,
                             lemma_lexicon: Optional[object] = None) -> Tuple[object, object]:

    """ Build a wordform and a lemma lexicons out of Giella data, based on the Zaliznyak dictionary. """

    source = open(path, 'r', encoding='utf8')
    if not wordform_lexicon:
        wordform_lexicon = clexicon_pb2.Lexicon()
    if not lemma_lexicon:
        lemma_lexicon = clexicon_pb2.Lexicon()

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
        wordform_lexicon = _build_entry(wordform_lexicon, key='wordform', add_wordform=unstressed,
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
            lemma_lexicon = _build_entry(lemma_lexicon, key='lemma', add_lemma=lemma,
                                               source='zaliznyak-giella',
                                               morph_features=features, add_clitic=clitic,
                                               add_clitic_features=clitic_features,
                                               add_segments=pron_segments)
    source.close()

    return wordform_lexicon, lemma_lexicon
