# -*- coding: utf-8 -*-
# Copyright 2019 Craig Thorburn

"""
Created on Mon May 6 15:05:00 2019
@author: Craig Thorburn
"""
## PARAMETERS
corpus = 'WSJ'
matched = 'GPJ'
min_length = 2
max_length = 5
sample_size = 12

# CODE

import codecs
import os
import numpy as np
from nltk.tokenize import word_tokenize


def get_item_stats(data_folder, text_file, lexicon_file, item_folder,
                            item_file, output_file):
    """
    """
    os.chdir(data_folder)
    


    with codecs.open(lexicon_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    lexicon={}
    for l in lines:
        u = l.split(None, 1)
        lexicon[u[0]] = u[1]
    print('lexicon file loaded')
    
    with codecs.open(text_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines() 
    text={}
    for l in lines:
        t = l.split(None, 1)
        transcription = []
        for w in t[1].split():
            if w not in lexicon.keys():
                print(w+' not in lexicon')
                continue
            if w == 'NSN' or w == 'SPN':
                continue
            if lexicon[w] not in transcription:
                transcription.append(lexicon[w])       
        text[t[0]] = set(transcription)
    print('text file loaded')
    
    os.chdir(item_folder) 
    speakers = []
    items = {}           
    with codecs.open(item_file, mode='r', encoding='UTF-8') as inp:
        inp.readline()
        lines = inp.read().splitlines()
    for l in lines:
        i = l.split()
        spkr = i[3]
        utt = i[0]
        if spkr in items.keys():
            items[spkr].append(utt)
        else:
            speakers.append(spkr)
            items[spkr] = [utt]
    print('item file loaded')

    ax_total = 0
    bx_total = 0
    total_tasks = 0
    length = 0
    total_utts = 0
    for s1 in speakers:
#        print(s1)
        for s2 in speakers:
#            print(s2)
            if s1 == s2:
                continue
            
            s1_utts = items[s1]
            s2_utts = items[s2]
#            print(s1_utts)
#            print(s2_utts)
            for X in s1_utts:
#                print(X)
                for A in s1_utts:
                    length+=len(text[A])
                    total_utts+=1
#                    print(A)
                    if X==A:
                        continue
                    for B in s2_utts:
#                        print(B)
#                        print(text[A])
#                        print(text[B])
#                        print(text[X])
                        total_tasks += 1
                        ax_total+=len(text[A] & text[X])
                        bx_total+=len(text[B] & text[X])
#                        print(ax_total)
#                        print(bx_total)
#                        input()
                        
                        
                        
    

    print('done')
    
    print('ax overlap: '+str(float(ax_total)/total_tasks))
    print('bx overlap: '+str(float(bx_total)/total_tasks))
    print('average length: '+str(float(length)/total_utts))            
# Testing
#data_folder= 'D:\\files\\research\\projects\\lf\\ivector\\test'
#item_folder= 'D:\\files\\research\\projects\\lf\\ivector\\test'
#lexicon_file = 'lexicon.txt'
#text_file = 'text.txt'
#item_file = 'test.item'
#output_file = 'test.item_stats'
# generate_utterance_item(root, segments_file, text_file, utt2spk_file, 
#                            output_file)




data_folder = '/fs/clip-realspeech/corpora/spock-format/' + corpus + '/' + matched + '_matched_data_test/'
item_folder = '/fs/clip-realspeech/projects/lfe/eval/utt_abx/items/'
text_file = 'text.txt'
lexicon_file = 'lexicon.txt'
item_file = corpus + '_sample'+str(sample_size)+'_norej_min'+str(min_length)+'_max'+str(max_length)+'.item'
output_file = item_file+'_stats'


get_item_stats(data_folder, text_file, lexicon_file, item_folder,
                            item_file, output_file)

