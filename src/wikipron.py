from typing import Optional
import utils
import clexicon_v01_pb2


def compile_wikipron(path: str,
                     wordform_lexicon: Optional[object] = None) -> object:

    """ can only be built on wordforms """

    if not wordform_lexicon:
        wordform_lexicon = clexicon_v01_pb2.CLexicon()

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
            wordform_lexicon = utils._build_entry(wordform_lexicon, key='wordform',
                                                  add_wordform=wordform, source='wikipron',
                                                  add_phones=phones)

    return wordform_lexicon
