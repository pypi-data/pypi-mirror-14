# pyaramorph, an Arabic morphological analyzer
# Copyright © 2005 Alexander Lee
# Ported to Python from Tim Buckwalter's aramorph.pl.

import sys
import re
from pkg_resources import resource_filename
from . import buckwalter

# Data file paths
TABLE_AB = "tableAB"
TABLE_BC = "tableBC"
TABLE_AC = "tableAC"
DICT_PREFIXES = "dictPrefixes"
DICT_STEMS = "dictStems"
DICT_SUFFIXES = "dictSuffixes"

def _data_file_path(filename):
    """ Return the path to the given data file """
    return resource_filename(__name__, filename)

def _tokenize(text):
    """ Extract all Arabic words from input and ignore everything
    else """
    tokens = re.split('[^\u0621-\u0652\u0670-\u0671]+', text)
        # include all strictly Arabic consonants and diacritics --
        # perhaps include other letters at a later time.
    return tokens

def _clean_arabic(text):
    """ Remove any تَطوِيل and vowels/diacritics """
    return re.sub('[\u0640\u064b-\u0652\u0670]', '', text)
    # FIXME do something about \u0671, ALIF WASLA ?

class Analyzer:

    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.out = out
        self.err = err
        self.seen = {}

        self.tableAB = self.load_table(TABLE_AB)
        self.tableBC = self.load_table(TABLE_BC)
        self.tableAC = self.load_table(TABLE_AC)

        self.prefixes = self.load_dict(DICT_PREFIXES)
        self.stems = self.load_dict(DICT_STEMS)
        self.suffixes = self.load_dict(DICT_SUFFIXES)

    def process(self, text):
        """ Extract Arabic words from the given text and analyze them
        """
        tokens = _tokenize(text.strip())
        for token in tokens:
            token = _clean_arabic(token)
            buckword = buckwalter.uni2buck(token)
            self.out.write("analysis for: %s %s\n" % (token, buckword))
            self.analyze(buckword)

    def analyze(self, word):
        """ Find possible solutions for the given word """
        results = []
        count = 0
        segments = self.segment(word)

        for prefix, stem, suffix in segments:
            if prefix in self.prefixes \
                    and stem in self.stems \
                    and suffix in self.suffixes:
                solutions = self.check_segment(prefix, stem, suffix)
                if len(solutions) > 0:
                    results += solutions

        if len(results) > 0:
            for solution in results:
                self.out.write(solution)
                self.out.write('\n')

    def check_segment(self, prefix, stem, suffix):
        """ See if the prefix, stem, and suffix are compatible """
        solutions = []

        # Loop through the possible prefix entries
        for pre_entry in self.prefixes[prefix]:
            (voc_a, cat_a, gloss_a, pos_a) = pre_entry[1:5]

            # Loop through the possible stem entries
            for stem_entry in self.stems[stem]:
                (voc_b, cat_b, gloss_b, pos_b, lemmaID) = stem_entry[1:]

                # Check the prefix + stem pair
                pairAB = "%s %s" % (cat_a, cat_b)
                if not pairAB in self.tableAB: continue

                # Loop through the possible suffix entries
                for suf_entry in self.suffixes[suffix]:
                    (voc_c, cat_c, gloss_c, pos_c) = suf_entry[1:5]

                    # Check the prefix + suffix pair
                    pairAC = "%s %s" % (cat_a, cat_c)
                    if not pairAC in self.tableAC: continue

                    # Check the stem + suffix pair
                    pairBC = "%s %s" % (cat_b, cat_c)
                    if not pairBC in self.tableBC: continue

                    # Ok, it passed!
                    buckvoc = "%s%s%s" % (voc_a, voc_b, voc_c)
                    univoc = buckwalter.buck2uni(buckvoc)
                    if gloss_a == '': gloss_a = '___'
                    if gloss_c == '': gloss_c = '___'
                    solutions.append(
                        "    solution: (%s %s) [%s]\n"
                        "         pos: %s%s%s\n"
                        "       gloss: %s + %s + %s\n" % \
                        (univoc, buckvoc, lemmaID, \
                        pos_a, pos_b, pos_c, \
                        gloss_a, gloss_b, gloss_c))

        return solutions

    def segment(self, word):
        """ Create possible segmentations of the given word """
        segments = []
        prelen = 0
        suflen = 0
        strlen = len(word)

        while prelen <= 4:
            # This loop increases the prefix length until > 4
            prefix = word[0:prelen]
            stemlen = strlen - prelen
            suflen = 0

            while stemlen >= 1 and suflen <= 6:
                # This loop increases suffix length until > 6,
                # or until stem length < 1
                stem = word[ prelen : (prelen+stemlen) ]
                suffix = word[ (prelen+stemlen) : ]
                segments.append( (prefix, stem, suffix) )
                
                stemlen -= 1
                suflen += 1

            prelen += 1

        return segments

    def load_dict(self, filename, encoding='latin1'):
        """ Load the given dictionary file """
        dict = {}
        lemmas = 0
        entries = 0
        lemmaID = ""

        p_AZ = re.compile('^[A-Z]')
        p_iy = re.compile('iy~$')

        infile = open(_data_file_path(filename), 'r', encoding=encoding)
        self.out.write("loading %s ... " % (filename))

        for line in infile:
            if line.startswith(';; '): # a new lemma
                m = re.search('^;; (.*)$', line)
                lemmaID = m.group(1)
                if lemmaID in self.seen:
                    self.err.write("lemmaID %s in %s isn't unique!\n" %
                            (lemmaID, filename))
                    sys.exit(1)
                else:
                    self.seen[lemmaID] = 1;
                    lemmas += 1;

            elif line.startswith(';'): # a comment
                continue

            else: # an entry
                line = line.strip(' \n')
                (entry, voc, cat, glossPOS) = re.split('\t', line)

                m = re.search('<pos>(.+?)</pos>', glossPOS)
                if m:
                    POS = m.group(1)
                    gloss = glossPOS
                else:
                    gloss = glossPOS
                    #voc = "%s (%s)" % (buckwalter.buck2uni(voc), voc)
                    if cat.startswith('Pref-0') or cat.startswith('Suff-0'):
                        POS = "" # null prefix or suffix
                    elif cat.startswith('F'):
                        POS = "%s/FUNC_WORD" % voc
                    elif cat.startswith('IV'):
                        POS = "%s/VERB_IMPERFECT" % voc
                    elif cat.startswith('PV'):
                        POS = "%s/VERB_PERFECT" % voc
                    elif cat.startswith('CV'):
                        POS = "%s/VERB_IMPERATIVE" % voc
                    elif cat.startswith('N') and p_AZ.search(gloss):
                        POS = "%s/NOUN_PROP" % voc # educated guess
                                # (99% correct)
                    elif cat.startswith('N') and p_iy.search(voc):
                        POS = "%s/NOUN" % voc # (was NOUN_ADJ:
                                # some of these are really ADJ's
                                # and need to be tagged manually)
                    elif cat.startswith('N'):
                        POS = "%s/NOUN" % voc
                    else:
                        self.err.write("no POS can be deduced in %s!\n" % filename)
                        self.err.write(line+'\n')
                        sys.exit(1)

                gloss = re.sub('<pos>.+?</pos>', '', gloss)
                gloss = gloss.strip()

                dict.setdefault(entry, []).append(
                    (entry, voc, cat, gloss, POS, lemmaID))
                entries += 1

        infile.close()
        if not lemmaID == "":
            self.out.write(
                "loaded %d lemmas and %d entries\n" % (lemmas, entries))
        else:
            self.out.write("loaded %d entries\n" % (entries))
        return dict

    def load_table(self, filename, encoding='latin1'):
        """ Load the given table file """
        p = re.compile('\s+')
        table = {}
        infile = open(_data_file_path(filename), 'r', encoding=encoding)

        for line in infile:
            if line.startswith(';'): continue # comment line
            line = line.strip()
            p.sub(' ', line)
            table[line] = 1

        infile.close()
        return table

