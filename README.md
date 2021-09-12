# RusLex

RusLex is a databse of Russian lexicon that combines data from 4 sources. The data include morphological and pronunciation analyses.

## NEW! Data on novel Russian loanwords is coming soon!

The sources are:

- Giella (based on the Zaliznyak dictionary)
  - https://github.com/giellalt/lang-rus
- WikiPron
  - https://github.com/kylebgorman/wikipron
- UniMoprh
  - https://github.com/unimorph/rus
- Apertium (the lexicon excludes multi-word entries)
    - https://github.com/apertium/apertium-rus

## installation

To install, clone the repo and run:

```shell
pip install -e .
```

After that, the data can be imported as follows:
```python
from ruslex import clexicon

wordform_lexicon = clexicon.wordform_lexicon()
lemma_lexicon = clexicon.lemma_lexicon()
```

## format

The PB structure of the data is described in the ```clexicon.proto``` file.
The data can be looped through as e.g.:
```python
from google.protobuf import text_format

for key in lexicon.analyses:
	if key == "Августович":
		print("Data format:")
		print(text_format.MessageToString(lexicon.analyses[key], as_utf8=True))
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
```


## data

If interested, the compiled data are also provided in the ``` data``` folder, as 2 lexicons:
- the lemma lexicon, where the keys are lemmas, and the values are the corresponding morphological and pronunctiation data 
- the wordform lexicon, where the keys are wordforms, and the values are their lemmas (where available), the correposnding morphological  and pronunciation data

The ```.textproto``` file contains the data in a human readable format

## license

The codebase is distributed under the GNU General Public License v3 (GPLv3). Please see ```License.txt``` for details.

The data sources used bear their original licenses.





