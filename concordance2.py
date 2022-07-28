from collections import Counter, defaultdict, namedtuple
from enum import auto
import os

directory_path = os.getcwd()
ConcordanceLine = namedtuple(
    "ConcordanceLine",
    ["left", "query", "right", "offset", "left_print", "right_print", "line"],
)

class ConcordanceIndex:
    def __init__(self, tokens, key=lambda x: x):
        self._tokens = tokens
        """The document (list of tokens) that this concordance index
           was created from."""

        self._key = key
        """Function mapping each token to an index key (or None)."""

        self._offsets = defaultdict(list)
        """Dictionary mapping words (or keys) to lists of offset indices."""
        # Initialize the index (self._offsets)
        for index, word in enumerate(tokens):
            word = self._key(word)
            self._offsets[word].append(index)


    def tokens(self):
        return self._tokens


    def offsets(self, word):
        word = self._key(word)
        return self._offsets[word]


    def __repr__(self):
        return "<ConcordanceIndex for %d tokens (%d types)>" % (
            len(self._tokens),
            len(self._offsets),
        )

    def find_concordance(self, word, width=auto):
        if isinstance(word, list):
            phrase = word
        else:
            phrase = [word]

        half_width = (width - len(" ".join(phrase)) - 2) // 2
        context = width // 4  # approx number of words of context

        # Find the instances of the word to create the ConcordanceLine
        concordance_list = []
        offsets = self.offsets(phrase[0])
        for i, word in enumerate(phrase[1:]):
            word_offsets = {offset - i - 1 for offset in self.offsets(word)}
            offsets = sorted(word_offsets.intersection(offsets))
        if offsets:
            for i in offsets:
                query_word = " ".join(self._tokens[i : i + len(phrase)])
                # Find the context of query word.
                left_context = self._tokens[max(0, i - context) : i]
                right_context = self._tokens[i + len(phrase) : i + context]
                # Create the pretty lines with the query_word in the middle.
                left_print = " ".join(left_context)[-half_width:]
                right_print = " ".join(right_context)[:half_width]
                # The WYSIWYG line of the concordance.
                line_print = " ".join([left_print, query_word, right_print])
                # Create the ConcordanceLine
                concordance_line = ConcordanceLine(
                    left_context,
                    query_word,
                    right_context,
                    i,
                    left_print,
                    right_print,
                    line_print,
                )
                concordance_list.append(concordance_line)
        return concordance_list


    def print_concordance(self, word, width=80, lines=auto):
        concordance_list = self.find_concordance(word, width=width)

        if not concordance_list:
            print("no matches")
        else:
            lines = min(lines, len(concordance_list))
            print(f"Displaying {lines} of {len(concordance_list)} matches:")
            for i, concordance_line in enumerate(concordance_list[:lines]):
                print(concordance_line.line)

class Text:
    _COPY_TOKENS = True
    def __init__(self, tokens, name=None):
        if self._COPY_TOKENS:
            tokens = list(tokens)
        self.tokens = tokens
        self.countTokens = len(tokens)
        # print(f"{self.countTokens} tokens in the text")
        if name:
            self.name = name
        elif "]" in tokens[:20]:
            end = tokens[:20].index("]")
            self.name = " ".join(str(tok) for tok in tokens[1:end])
        else:
            self.name = " ".join(str(tok) for tok in tokens[:8]) + "..."

    def concordance_list(self, word, width=80, lines=2000):
        if "_concordance_index" not in self.__dict__:
            self._concordance_index = ConcordanceIndex(
                self.tokens, key=lambda s: s.lower()
            )
        return self._concordance_index.find_concordance(word, width)[:lines]