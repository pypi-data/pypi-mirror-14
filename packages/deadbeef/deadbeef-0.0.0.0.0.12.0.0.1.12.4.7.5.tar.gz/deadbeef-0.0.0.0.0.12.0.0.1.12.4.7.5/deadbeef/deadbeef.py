_standard_replacements = {
    'g': '9',
    'i': '1',
    'j': 'f',
    'o': '0',
    's': '5',
    't': '7',
    'z': '2',
}

# these replacements are ambiguous, but that's ok, cause there are collisions anyways!
_ambiguous_replacements = {
    'l': '1',
    'q': '9',
}

# these replacements make the text look a bit weird
_weird_replacements = {
    'h': '6',
}

# no replacements for these :-(
#   'k':
#   'm':
#   'n':
#   'p':
#   'r':
#   'u':
#   'v':
#   'w':
#   'x':
#   'y':

import re
import random

class DEADBEEF(object):
    """
    This is the workhorse of the deadbeef module. It generates hexspeak from dictionaries.
    """

    def __init__(self, extra_allowed=None, replacements=None, ambiguous=True, weird=True, dictpath="/usr/share/dict/words"):
        """
        Initializes a DEADBEEF object.

        :param iterable extra_allowed: add extra characters that can be permitted (other than "0123456789abcdef")
        :param mapping replacements: a dictionary of replacements (i.e., 'i' -> '1'). If None, standard replacements are used.
        :param ambiguous: use ambiguous replacements (i.e., '1' for both 'i' and 'l')
        :param weird: use replacements that seem weird (i.e., '6' for 'g')
        :param dictpath: the path to the wordlist to use (default "/usr/share/dict/words")
        """

        self.allowed = set("0123456789abcdef")
        if extra_allowed:
            self.allowed.update(extra_allowed)

        if replacements is None:
            self.replacements = dict(_standard_replacements)
            if ambiguous:
                self.replacements.update(_ambiguous_replacements)

            if weird:
                self.replacements.update(_weird_replacements)
        else:
            self.replacements = replacements

        self.allowed.update(self.replacements.keys())

        self._pattern = re.compile(r'|'.join(self.replacements.keys()))
        self._dictpath = dictpath
        self._dictfile = open(dictpath)

    def _convert(self, s):
        # grabbed from http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
        return self._pattern.sub(lambda x: self.replacements[x.group()], s)

    def _is_allowed(self, s):
        return len(set(s) - self.allowed) == 0

    def _normal_words(self, stop_at=None):
        for line in self._dictfile:
            if stop_at is None:
                stop_at = line
            elif line == stop_at:
                return

            for word in line.split():
                wl = word.lower()
                if self._is_allowed(wl):
                    yield wl

        self._dictfile.close()
        self._dictfile = open(self._dictpath)
        for w in self._normal_words(stop_at=stop_at):
            yield w

    def skip(self, n=None):
        """
        Skip some number of words from the dictionary.

        :param n: the number of words to skip (if None, a random value between 0 and 4000)
        """

        try:
            for _ in zip(xrange(random.randint(0, 4000) if n is None else n), self._normal_words()): pass
        except NameError:
            # why the fuck would you do this to your own language?
            for _ in zip(range(random.randint(0, 4000) if n is None else n), self._normal_words()): pass


    def candidate_count(self):
        """
        Returns the number of potential candidate words in the wordlist.
        """

        return len(list(self._normal_words()))

    def _get_word_pair(self, length=None, prefilter=None, postfilter=None):
        for w in self._normal_words():
            if length is not None and len(w) != length:
                continue

            if prefilter is not None and not prefilter(w):
                continue

            hw = self._convert(w)

            if postfilter is not None and not postfilter(hw):
                continue

            return w, hw

        raise BADC0DE("f411ed 70 f1nd hex5peak")

    def get_string(self, length=None, prefilter=None, postfilter=None):
        """
        Gets a hexstring from the wordlist, in string form.

        :param int length: the length of the string. If None, any length.
        :param function prefilter: a filter function to apply on the candidate (non-hex) strings
        :param function postfilter: a filter function to apply on the output (hex) strings
        :returns: a hexstring (in string form)
        """
        return self._get_word_pair(length=length, prefilter=prefilter, postfilter=postfilter)[1]

    def get_int(self, length=None, prefilter=None, postfilter=None):
        """
        Gets a hexstring from the wordlist, in integer form.

        :param int length: the number of *hex letters* in the string (i.e., twice the number of bytes).
                           If None, any length.
        :param function prefilter: a filter function to apply on the candidate (non-hex) strings
        :param function postfilter: a filter function to apply on the output (hex) strings
        :returns: a integer that, when viewed as hex, is hexspeak
        """
        return int(self._get_word_pair(length=length, prefilter=prefilter, postfilter=postfilter)[1], 16)

class BADC0DE(Exception):
    pass
