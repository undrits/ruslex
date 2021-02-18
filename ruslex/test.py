#!usr/bin/env python

from ruslex import clexicon

lexicon = clexicon.wordform_lexicon()

for key in lexicon.analyses:
	if key == 'ребята':
		print(lexicon.analyses[key])
