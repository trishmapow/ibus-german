from fuzzywuzzy import process, fuzz
from ast import literal_eval

words = list()
with open('parsed_dictcc.txt', 'r') as dictdata:
    iterdict = iter(dictdata)
    next(iterdict)
    for line in iterdict:
        start = line.index('\"') + 1
        end = line.index('\"', start)
        words.append(line[start:end])

print(f'{len(words)} words')
try:
    while True:
        print(process.extract(input("search> "), words, limit=2, scorer=fuzz.QRatio))
except KeyboardInterrupt:
    print()
    pass