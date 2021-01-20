from typing import List, Optional


def _build_entry(lexicon: object,
                 key: str = 'wordform', # or 'lemma'
                 add_wordform: Optional[str] = None,
                 add_lemma: Optional[str] = None,
                 morph_source: Optional[str] = None,
                 morph_features: Optional[List[str]] = None,
                 add_clitic: Optional[str] = None,
                 add_clitic_features: Optional[List[str]] = None,
                 add_stressed: Optional[str] = None,
                 stressed_source: Optional[str] = None,
                 pron_source: Optional[str] = None,
                 add_phones: Optional[List[str]] = None,
                 add_syllables: Optional[List[str]] = None,
                 ) -> object:

    # wordform lexicon
    if key == 'wordform':
        entry = ''
        # if lemma is provided, check if an entry with the same wordform and lemma
        # already exists in the lexicon, and if so - add to it
        if add_lemma:
            for analysis in lexicon.analyses[add_wordform].analysis:
                if analysis.lemma == add_lemma:
                    entry = analysis
            if not entry:
                entry = lexicon.analyses[add_wordform].analysis.add()
                entry.lemma = add_lemma
        else:
            entry = lexicon.analyses[add_wordform].analysis.add()

    # lemma lexicon
    elif key == 'lemma':
        assert add_lemma, 'No lemma provided for the lemma lexicon'
        # if lemma is provided, check if an entry with the same lemma
        # already exists in the lexicon, and if so - add to it
        if lexicon.analyses[add_lemma].analysis:
            entry = lexicon.analyses[add_lemma].analysis[0]
        else:
            entry = lexicon.analyses[add_lemma].analysis.add()

    # adding morphological features
    if morph_features:
        morphology = entry.morphology.add()
        assert morph_source, "No source provided for the morph_features"
        morphology.source = morph_source
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
    if add_stressed:
        if entry.pronunciation:
            if entry.pronunciation[0].stress != add_stressed:
                pronunciation = entry.pronunciation.add()
                assert stressed_source, "No source provided for the stressed form"
                pronunciation.source = stressed_source
                pronunciation.stress = add_stressed
        else:
            pronunciation = entry.pronunciation.add()
            assert stressed_source, "No source provided for the stressed form"
            pronunciation.source = stressed_source
            pronunciation.stress = add_stressed
    if add_phones:
        pronunciation = entry.pronunciation.add()
        assert pron_source, "No source provided for the stressed form"
        pronunciation.source = pron_source
        pronunciation.phone.extend(add_phones)
    # no syllable data so far - might need correcting if a source has both phones and syllables
    if add_syllables:
        pronunciation = entry.pronunciation.add()
        assert pron_source, "No source provided for the stressed form"
        pronunciation.source = pron_source
        pronunciation.phone.extend(add_syllables)

    return lexicon
