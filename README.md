# russian lexicon

Russian lexicon data from 4 sources. The data include morphological and pronunciation analyses.

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
    # key is the wordform or lemma
    # to loop through analyses associated with each key
    for analysis in lexicon.analyses[key].analysis:
        # to see source
        print(text_format.MessageToString(analysis.source, as_utf8=True))
        # to print the morphology data
        print(text_format.MessageToString(analysis.morphology, as_utf8=True))
        # to access the pronunciation data
        for prons in analysis.pronunciation:
            print(text_format.MessageToString(prons, as_utf8=True))
```


## data

If interested, the compiled data are also provided in the ``` data``` folder, as 2 lexicons:
- the lemma lexicon, where the keys are lemmas, and the values are the corresponding morphological and pronunctiation data 
- the wordform lexicon, where the keys are wordforms, and the values are their lemmas (where available), the correposnding morphological  and pronunciation data

The ```.textproto``` file contains the data in a human readable format

## license

The codebase is distributed under the GNU General Public License v3 (GPLv3). Please see ```License.txt``` for details.

The data sources used bear their original licenses.





