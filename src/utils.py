from typing import List, Optional


def _build_entry(lexicon: object,
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
    ''' Internal function for building the protobuf lexicon entry '''
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
        morphology = entry.morphology.add()
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
    if add_phones:
        pronunciation = entry.pronunciation.add()
        pronunciation.phone.extend(add_phones)
    if add_segments:
        pronunciation = entry.pronunciation.add()
        pronunciation.segment.extend(add_segments)
    # no syllable data so far
    if add_syllables:
        pronunciation = entry.pronunciation.add()
        pronunciation.phone.extend(add_syllables)

    return lexicon
