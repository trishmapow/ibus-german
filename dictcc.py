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
    def __init__(self, input_file="dictcc.txt", output_file="parsed_dictcc.txt"):
        self.input_file = input_file
        self.output_file = "de_" + output_file
        self.output_file_en = "en_" + output_file

        try:
            self.num_words = int(linecache.getline(self.output_file, 1))
        except ValueError:                          # file doesn't exist
            print(f"First run, parsing {self.input_file}... (may take a moment)")
            words = self.parse_txt(debug=True)
            words.sort(key=lambda w: w.de.lower())  # sort lower before uppercase
            self.num_words = len(words)

            words_en = sorted(words, key=lambda w: w.en.lower())    # sort by english word

            with open(self.output_file, "w") as f, open(self.output_file_en, "w") as f_en:
                length = f"{self.num_words}\n"      # save file length for efficiency

                # save eval-able list
                format_output = lambda word: (f'["{word.de}", "{word.en}", {word.gender}, {word.w_type}, '
                                f"{word.categories}, {word.en_tags}, {word.de_tags}]\n")
                print(f"Writing to {self.output_file}...")
                f.write(length)
                for word in words:
                    f.write(format_output(word))

                print(f"Writing to {self.output_file_en}")
                f_en.write(length)
                for word in words_en:
                    f_en.write(format_output(word))
            del words
            print("Parsing and saving complete.")

    def get_word(self, index, lang='DE'):
        try:
            path = self.output_file if lang == 'DE' else self.output_file_en
            return Word(
                *literal_eval(linecache.getline(path, index + 2).strip())
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

        with open(self.input_file, encoding="utf-8") as dictdata:
            count = failed = 0
            for line in dictdata:
                line = re.sub(r"\t+", ";", html.unescape(line))
                match = re.match(regex, line)
                if match:
                    m_dict = {k: v.strip() for k, v in match.groupdict(default="").items()}
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

    def words_starting_with(self, s, num=40, lang='DE'):
        l_index = self.search(s, lang=lang)
        result = list()
        for i in range(l_index, l_index + num):
            word = self.get_word(i, lang=lang)
            if lang == 'DE':
                text = str(word)
            else:
                text = str(word).split(' => ')
                text = text[1] + ' => ' + text[0]
            result.append((word.de, text))
        return result

    def search(self, target, lo=0, hi=None, lang='DE'):
        if lo < 0:
            raise ValueError("lo must be non-negative")
        if hi is None:
            hi = self.num_words
        while lo < hi:
            mid = (lo + hi) // 2
            word = self.get_word(mid, lang=lang)
            compare = word.de if lang == 'DE' else word.en
            if compare.lower() < target.lower():
                lo = mid + 1
            else:
                hi = mid
        return lo


if __name__ == "__main__":
    d = DictParser()
    language = input("Language (DE or EN): ")
    try:
        while True:
            results = d.words_starting_with(input("Search: "), lang=language)
            print(f"first: {results[0]} last: {results[-1]}")
    except KeyboardInterrupt:
        exit()
