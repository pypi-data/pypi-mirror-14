'''
Created on Feb 19, 2016

@author: mike
'''
import codecs
from patgen import parse_patterns, apply_patterns, load_project, load_dictionary,\
    parse_dictionary_word

#word = 'а҆в-ва-кꙋ́-момъ'
word = 'а҆ввакꙋ́момъ'
word = 'всеѧ̀'

def read_patterns(fname):
    with codecs.open(fname, 'r', 'utf-8') as f:
        for l in f:
            l = l.strip()
            if l == '}':
                break
            if l == '\\patterns{':
                continue
            yield l

project = load_project('words')

for x in read_patterns('words.tex'):
    print (x)

patterns = parse_patterns(read_patterns('words.tex'))
print(len(patterns))

prediction = apply_patterns(patterns, word, 10)
print(prediction)
print(word.encode('unicode-escape'))

prediction = apply_patterns(project.patterns, word, 10)
print(prediction)
print(word.encode('unicode-escape'))

allkeys = set()
for patternset in project.patterns:
    allkeys.update(patternset.keys())

allkeys_new = set()
for patternset in project.patterns:
    allkeys_new.update(patternset.keys())

assert allkeys == allkeys_new

dicti = load_dictionary('words.txt')

print ('DICTI:', dicti[word])
print (parse_dictionary_word('вс-еѧ̀'))

for key in sorted(allkeys):
    # optimize predictive patterns
    for i in range(0, len(project.patterns)):
        patts = project.patterns[i][key]
        for j in range(i+1, len(project.patterns)):
            patts -= project.patterns[j][key]

        if patts != patterns[i][key]:
            print(key, i, patts, patterns[i][key], project.patterns[i][key])
            assert False
