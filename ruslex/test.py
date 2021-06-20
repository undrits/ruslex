#!usr/bin/env python

from ruslex import clexicon


def test():
    lexicon = clexicon.wordform_lexicon()

    for key in lexicon.analyses:
        if key == "Августович":
            print("Data format:")
            print(lexicon.analyses[key])
            for analysis in lexicon.analyses[key].analysis:
                print("Data source:", analysis.source)
                print()
                print("All morphological features:", analysis.morphology.morph_features)
                print("Individual morphological features:")
                for feature in analysis.morphology.morph_features:
                    print(feature)
                print()
                for pron in analysis.pronunciation:
                    print("Pronunciation (phonetic):", pron.phone)
                    print("Phones:")
                    for phone in pron.phone:
                        print(phone)
                    print()
                    print("Pronunciation (orthographic with stress):", pron.segment)
                    print("Segments (with stress):")
                    for segment in pron.segment:
                        print(segment)
                    print()


if __name__ == "__main__":
    test()
