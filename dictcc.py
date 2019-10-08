import re
import linecache
import html
from ast import literal_eval

from recordclass import make_dataclass

Word = make_dataclass(
    "Word", ("de", "en", "gender", "w_type", "categories", "en_tags", "de_tags")
)
Word.__str__ = lambda self: (
    f"({' '.join(self.gender)}) {self.de} [{' '.join(self.de_tags)}] => "
    f"({' '.join(self.w_type)}) {self.en} [{' '.join(self.en_tags)}]"
)


class DictParser:
    def __init__(self, path_to_txt="dictcc.txt", path_to_parsed="parsed_dictcc.txt"):
        self.path_to_txt = path_to_txt
        self.path_to_parsed = path_to_parsed

        try:
            self.num_words = int(linecache.getline(self.path_to_parsed, 1))
        except ValueError:                          # file doesn't exist
            words = self.parse_txt(debug=True)
            words.sort(key=lambda w: w.de.lower())  # sort lower before uppercase
            self.num_words = len(words)
            with open(self.path_to_parsed, "w") as f:
                f.write(f"{self.num_words}\n")      # save file length for efficiency
                for word in words:                  # save eval-able list
                    f.write(
                        f'["{word.de}", "{word.en}", {word.gender}, {word.w_type}, '
                        f"{word.categories}, {word.en_tags}, {word.de_tags}]\n"
                    )
            del words

    def get_word(self, index):
        try:
            return Word(
                *literal_eval(linecache.getline(self.path_to_parsed, index + 2).strip())
            )
        except (SyntaxError, TypeError) as e:
            print(e)
            return Word("SyntaxError parsing", "", [], [], [], [], [])

    def parse_txt(self, debug=False):
        words = list()
        regex = re.compile(
            r"""^(?P<de_extra>\(.*?\)\s)?               # bracketed extra info
                 (?P<de>[^\{\[;]+)\s?                   # DE word
                 (?P<gender>(?:\{(?:m|f|n|pl)\}\s?)*)   # m/f/n/pl gender(s)
                 (?P<de_tags>(?:\[.+?\]\s?)*)           # DE tag info in []
                 (?P<de_2>.*?);(?P<en>[^\[]+?)          # sometimes DE word split, combine with <de>
                 (?P<en_tags>(?:\[.+?\]\s?)*);          # EN tag info in []
                 (?P<type>(?:[^;\[\n])*);?              # word type(s)
                 (?P<tags>(?:\[.+?\]\s)*)               # word categor(y|ies)
            """,
            re.VERBOSE,
        )

        with open(self.path_to_txt, encoding="utf-8") as dictdata:
            count = failed = 0
            for line in dictdata.readlines():
                line = re.sub(r"\t+", ";", html.unescape(line))
                match = re.match(regex, line)
                if match:
                    m_dict = {k: v.strip() for k, v in match.groupdict(default="")}
                    words.append(
                        Word(
                            m_dict["de"] + m_dict["de_2"],
                            m_dict["en"],
                            DictParser.tags_to_list(m_dict["gender"], "{}"),
                            m_dict["type"].split(),
                            DictParser.tags_to_list(m_dict["tags"], "[]"),
                            DictParser.tags_to_list(m_dict["en_tags"], "[]"),
                            DictParser.tags_to_list(m_dict["de_tags"], "[]"),
                        )
                    )
                else:
                    failed += 1
                count += 1

        if debug:
            print(f"{failed}/{count} entries failed to match")

        return words

    @staticmethod
    def tags_to_list(s, brackets):
        return s.replace(brackets[0], "").replace(brackets[1], "").split()

    def words_starting_with(self, s, num=40):
        l_index = self.search(s)
        result = list()
        for i in range(l_index, l_index + num):
            word = self.get_word(i)
            result.append((word.de, str(word)))
        return result

    def search(self, x, lo=0, hi=None):
        if lo < 0:
            raise ValueError("lo must be non-negative")
        if hi is None:
            hi = self.num_words
        while lo < hi:
            mid = (lo + hi) // 2
            word = self.get_word(mid)
            if word.de.lower() < x.lower():
                lo = mid + 1
            else:
                hi = mid
        return lo


if __name__ == "__main__":
    d = DictParser()
    try:
        while True:
            results = d.words_starting_with(input("Search: "))
            print(f"first: {results[0]} last: {results[-1]}")
    except KeyboardInterrupt:
        exit()
