from ruslex import clexicon_pb2
import gzip

LEMMA_PATH = "data/lemma_lexicon.pb.gz"
WORDFORM_PATH = "data/wordform_lexicon.pb.gz"


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
