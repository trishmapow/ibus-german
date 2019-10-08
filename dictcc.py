from dataclasses import dataclass, field
from typing import List
from bisect import bisect_left
import re
import pickle
from functools import total_ordering

@dataclass
@total_ordering
class Word:
    
    de: str
    en: str = ''
    gender: List[str] = field(default_factory=list)
    w_type: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    en_tags: List[str] = field(default_factory=list)
    de_tags: List[str] = field(default_factory=list)

    def __lt__(self, other):
        return self.de.lower() < other.de.lower()

    def __str__(self):
        return f"'{self.de}' (DE) => '{self.en}' (EN)"

class DictParser:

    def __init__(self, path_to_txt="dictcc_unescaped.txt", path_to_pickle="parsed_dictcc"):
        self.path_to_txt = path_to_txt
        self.path_to_pickle = path_to_pickle
        self.words = list()

        try:
            with open(path_to_pickle, 'rb') as f:
                self.words = pickle.load(f)
        except FileNotFoundError:
            self.words = self.parse_txt(debug=True)
            with open(path_to_pickle, 'wb') as f:
                pickle.dump(self.words, f)
        else:
            print("Successfuly loaded pickled words")

    @staticmethod
    def tags_to_list(s, brackets):
        return s.replace(brackets[0], '').replace(brackets[1], '').split()

    def parse_txt(self, debug=False):
        words = list()
        """
        Processing raw dict.cc txt file:
        1) Unescape html numeric entities &#xxx (html.unescape())
        2) Find and replace '\t+' to ';'
        Final regex: https://regex101.com/r/Vnxr4Y/10
        """
        regex = re.compile(r'^(?P<de_extra>\(.*?\)\s)?(?P<de>[^\{\[;]+)\s?(?P<gender>(?:\{(?:m|f|n|pl)\}\s?)*)(?P<de_tags>(?:\[.+?\]\s?)*)(?P<de_2>.*?);(?P<en>[^\[]+?)(?P<en_tags>(?:\[.+?\]\s?)*);(?P<type>(?:[^;\[\n])*);?(?P<tags>(?:\[.+?\]\s)*)')

        with open(self.path_to_txt, encoding='utf-8') as dictdata:
            count = failed = 0
            for line in dictdata.readlines():
                match = re.match(regex, line)
                if match:
                    m_dict = match.groupdict(default="")
                    m_dict = {k: v.strip() for k, v in m_dict.items()}
                    words.append(Word(m_dict['de'] + m_dict['de_2'], m_dict['en'], DictParser.tags_to_list(m_dict['gender'], '{}'), m_dict['type'].split(), DictParser.tags_to_list(m_dict['tags'], '[]'), DictParser.tags_to_list(m_dict['en_tags'], '[]'), DictParser.tags_to_list(m_dict['de_tags'], '[]')))
                else:
                    failed += 1
                count += 1

        if debug:
            print(f"{failed}/{count} entries failed to match")

        return words

    def words_starting_with(self, s, num=10):
        l_index = bisect_left(self.words, s)
        return [self.words[i] for i in range(l_index, l_index + num) if self.words[i].de.lower().startswith(s.de)]

if __name__ == "__main__":
    d = DictParser()
    while True:
        print(d.words_starting_with(Word(input())))