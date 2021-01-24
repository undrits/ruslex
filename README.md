# rus_data

Russian lexicon data from 4 sources. The data include morphological and pronunciation analyses.

The sources are:

- Giella (based on the Zaliznyak dictionary)
  - https://github.com/giellalt/lang-rus
- WikiPron
  - https://github.com/kylebgorman/wikipron
- UniMoprh
  - https://github.com/unimorph/rus
- Apertium
    - https://github.com/apertium/apertium-rus


## data & format

The data are compiled into 2 lexicons:
- the lemma lexicon, where the keys are lemmas, and the values are the corresponding morphological and pronunctiation data 
- the wordform lexicon, where the keys are wordforms, and the values are their lemmas (where available), the correposnding morphological  and pronunciation data

The data is provided in 2 formats:
- .pb is a binary file that can be read by protobuf
- .textproto contains the data in a human readable format

The data sources used bear their original licenses.




