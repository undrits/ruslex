#! usr/bin/env python

""" Build RusLex lexicon out of multiple provided data sources (Zaliznyak-Giella, WikiPron, UniMorph, Apertium) """

import argparse
from google.protobuf import text_format
import clexicon_pb2
from utils import _compile_apertium, \
    _compile_unimorph, \
    _compile_wikipron, \
    _compile_zaliznyak_giella
import time


def read_lexicon(path: str) -> clexicon_pb2.Lexicon:
    lexicon = clexicon_pb2.Lexicon()
    f = open(path, "rb")
    lexicon.ParseFromString(f.read())
    f.close()
    return lexicon


def main(args: argparse.Namespace) -> None:

    # create wordform and lemma lexicons
    w_lexicon = clexicon_pb2.Lexicon()
    l_lexicon = clexicon_pb2.Lexicon()

    # add data from provided sources
    if args.zaliznyak_giella:
        w_lexicon, l_lexicon = _compile_zaliznyak_giella(args.zaliznyak_giella,
                                                        w_lexicon, l_lexicon)
    if args.wikipron:
        w_lexicon = _compile_wikipron(args.wikipron, w_lexicon)
    if args.unimorph:
        w_lexicon, l_lexicon = _compile_unimorph(args.unimorph, w_lexicon, l_lexicon)
    if args.apertium:
        w_lexicon, l_lexicon = _compile_apertium(args.apertium, w_lexicon, l_lexicon)

    # save to disk
    if args.lemma_lexicon:
        l_output = open(args.lemma_lexicon, 'wb')
    else:
        l_output = open('lemma_lexicon.pb', 'wb')
    l_output.write(l_lexicon.SerializeToString())
    l_output.close()

    if args.wordform_lexicon:
        w_output = open(args.wordform_lexicon, 'wb')
    else:
        w_output = open('wordform_lexicon.pb', 'wb')
    w_output.write(w_lexicon.SerializeToString())
    w_output.close()

    # save in a human readable format
    if args.lemma_lexicon_h:
        l_output_h = open(args.lemma_lexicon_h, 'w')
    else:
        l_output_h = open('lemma_lexicon.textproto', 'w')
    l_output_h.write(text_format.MessageToString(l_lexicon, as_utf8=True))
    l_output_h.close()

    if args.wordform_lexicon_h:
        w_output_h = open(args.wordform_lexicon_h, 'w')
    else:
        w_output_h = open('wordform_lexicon.textproto', 'w')
    w_output_h.write(text_format.MessageToString(w_lexicon, as_utf8=True))
    w_output_h.close()
    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zaliznyak_giella",
        required=False,
        help="path to the tsv file with the zaliznyak-giella data",
    )
    parser.add_argument(
        "--wikipron",
        required=False,
        help="path to the tsv file with the wikipron data",
    )
    parser.add_argument(
        "--unimorph",
        required=False,
        help="path to the tsv file with the unimorph data",
    )
    parser.add_argument(
        "--apertium",
        required=False,
        help="path to the tsv file with the apertium data",
    )
    parser.add_argument(
        "--lemma_lexicon",
        required=False,
        help="path for the binary lemma lexicon output",
    )
    parser.add_argument(
        "--lemma_lexicon_h",
        required=False,
        help="path for the human readable lemma lexicon output",
    )
    parser.add_argument(
        "--wordform_lexicon",
        required=False,
        help="path for the binary wordform lexicon output",
    )
    parser.add_argument(
        "--wordform_lexicon_h",
        required=False,
        help="path for the human readable wordform lexicon output",
    )

    main(parser.parse_args())
    print('Time:', time.process_time())

