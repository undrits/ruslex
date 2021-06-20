from ruslex import clexicon_pb2
import gzip
import os
from pathlib import Path

DIR = Path(__file__).resolve().parent
LEMMA_PATH = os.path.join(DIR, 'data', 'lemma_lexicon.pb.gz')
WORDFORM_PATH = os.path.join(DIR, 'data', 'wordform_lexicon.pb.gz')


def lemma_lexicon(path: str = LEMMA_PATH):
    """Returns the lemma lexicon"""
    lexicon = clexicon_pb2.Lexicon()
    with gzip.open(path, "rb") as byte_file:
        lexicon.ParseFromString(byte_file.read())
    return lexicon


def wordform_lexicon(path: str = WORDFORM_PATH):
    """Returns the wordform lexicon"""
    lexicon = clexicon_pb2.Lexicon()
    with gzip.open(path, "rb") as byte_file:
        lexicon.ParseFromString(byte_file.read())
    return lexicon
