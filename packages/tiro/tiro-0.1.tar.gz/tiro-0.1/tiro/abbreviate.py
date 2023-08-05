#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import re
import sys
from os import path

import yaml

from tiro.regnets import Regnet, Parser
from tiro.rules_generator import Generator


"""
Abba: The Abbreviation engine

This application works in several stages:

1. It reads abbreviation definitions written in the regnet markup from a .ini file.
2. It compiles each abbreviation definition into a regnet object in order to
   obtain a regexp and a precedence ranking.
3. It builds an abbreviation dictionary by:
    a. creating a new abbreviation object using the regexp and putting it into
       the correct order indicated by the precedence ranking.
    b. adding that abbreviation's rendering information to a lookup table.
4. It runs through a provided text, replacing matching patterns with single
   unicode control codepoints that are linked to abbreviation objects.
5. It renders the text according to the user's preference, referencing the
   control codepoints to the desired render method.

"""
__all__ = ["AbbreviationRegister"]

# Objects which represent abbreviation glyphs and can be regexped.
Abbreviation = collections.namedtuple("Abbreviation", "name, pattern, codepoint")


class AbbreviationRegister(object):

    """
    This object contains sequences of glyph transformations which it can run on
    text objects.
    """
    CONTROL_CHARS_START = 57344
    CONTROL_CHARS_END = 63743

    def __init__(self, abbreviations, encoding="uni_rep"):
        self.abb_sequences = []
        self.lookup_table = {}
        self.legend = {}
        # begin creating unicode characters at the beginning
        # of the private use space
        self.pool = range(self.CONTROL_CHARS_START, self.CONTROL_CHARS_END)
        # Read through the config file, pulling out abbreviation schemae
        for i, abbreviation in zip(self.pool, abbreviations):
            # Analyze the regnet markup and move it into the abbreviation dict
            codepoint = chr(i)
            regnet = Regnet(abbreviation["pattern"])
            name = abbreviation["name"]
            self.add_to_sequences(name, regnet, codepoint)

            value = abbreviation.get(encoding, name)
            self.lookup_table[codepoint] = value
            self.legend[name] = value

    def __getitem__(self, char):
        if self.CONTROL_CHARS_START <= ord(char) < self.CONTROL_CHARS_END:
            return self.lookup_table[char]
        else:
            return char

    def add_to_sequences(self, section, regnet_object, serial):
        """
        Given the makings of an abbreviation, create a new object
        and add it to the sequences list.
        """
        precedence = regnet_object.prec
        # build abb_sequences to the number of prec levels
        while len(self.abb_sequences) < precedence + 1:
            self.abb_sequences.append([])
        # add a new abbreviation object to the correct prec sequence
        self.abb_sequences[precedence].append(
            Abbreviation(section, regnet_object.pattern, serial))

    def abbreviate_text(self, text):
        """
        Runs each sequence of transforms in the order they were loaded into the
        controller.
        """
        for sequence in self.abb_sequences:
            for abbreviation in sequence:
                text = re.sub(abbreviation.pattern, abbreviation.codepoint, text)
        return text

    def generate_legend(self):
        return "\n".join("{}: {}"
                         .format(value, key)
                         for key, value in self.legend.items())

    def decode(self, text):
        return "".join(self[char] for char in text)


if __name__ == "__main__":
    dir_name = path.dirname(__file__)
    tna_filename = path.join(dir_name, "config", "tna.yml")
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate',
                        help="Analyze a text for frequency and generate abbreviations on the fly.",
                        action="store_true")
    parser.add_argument("--ruleset",
                        help="The ruleset to use. Uses The New Abbreviations if none is supplied.",
                        default=tna_filename)
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'))
    parser.add_argument('-t', '--text', nargs="+", help="""	The text to operate on.""")
    parser.add_argument('-r', '--render', help="Render method. Accepts 'unicode' or 'base'.",
                        default='unicode')
    parser.add_argument('-l', '--legend', help="Print a legend at the top of the text.",
                        action="store_true")
    args = parser.parse_args()

    # Determine input method
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip("\r\n")
    elif args.infile:
        text = (args.infile).read()
    elif args.text:
        text = " ".join(args.text)
    else:
        exit("No input received. Run 'python3 abbreviate.py -h' for more information.")

    # Get a ruleset and use it to generate an abbreviation register
    encoding = args.render
    if args.generate:
        ruleset = Generator(text).generate_rules()
    else:
        with open(args.ruleset, 'r') as f:
            ruleset = yaml.safe_load(f)
    parser = Parser(ruleset, encoding)
    abba = AbbreviationRegister(parser.abbreviations, encoding=encoding)

    # Choose the rendering method
    if args.legend:
        legend = abba.generate_legend()
        print(legend)

    abbreviated = abba.abbreviate_text(text)
    print(abba.decode(abbreviated))
