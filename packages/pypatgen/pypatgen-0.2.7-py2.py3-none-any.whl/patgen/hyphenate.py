'''
Created on Feb 24, 2016

@author: mike
'''
import codecs
import sys
from patgen import load_project, apply_patterns, format_dictionary_word

def main_hyphenate(args):
    
    project = load_project(args.project)
    
    maxchunk = 0
    for patternset in project.patterns:
        if patternset:
            maxchunk = max(maxchunk, max(len(x) for x in patternset.keys()))

    with codecs.open(args.input or sys.stdin.fileno(), 'r', 'utf-8') as f:
        with codecs.open(args.input or sys.stdin.fileno(), 'r', 'utf-8') as out:

            for word in f:
                word = word.strip()
    
                prediction = apply_patterns(project.patterns, word, maxchunk, 
                                            margin_left=project.margin_left, 
                                            margin_right=project.margin_right)
                
                s = format_dictionary_word(word, prediction)



    for word, hyphens in dictionary.items():

        if prediction != true_hyphens:
            yield word, prediction
            