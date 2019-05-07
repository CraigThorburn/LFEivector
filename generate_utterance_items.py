# -*- coding: utf-8 -*-
# Copyright 2019 Craig Thorburn

"""
Created on Mon May 6 15:05:00 2019
@author: Craig Thorburn
"""
## PARAMETERS
corpus = 'WSJ'
matched = 'GPJ'
sample_size = 12
rejection = False

# CODE

import codecs
import os
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

functionwords = stopwords.words('english')

def generate_utterance_item(input_folder, segments_file, text_file, utt2spk_file, 
                            output_folder, output_file, sample_size = 12, rejection = True):
    """
    """
    os.chdir(root)
    item_header = '#file onset offset #speaker text\n'
    
    with codecs.open(text_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    text={}
    for l in lines:
        t = l.split(maxsplit = 1)
        text[t[0]] = t[1]

    with codecs.open(utt2spk_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    utt2spk={}
    for l in lines:
        u = l.split(maxsplit = 1)
        utt2spk[u[0]] = u[1]
                
    with codecs.open(segments_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    

    speaker_dict = {}
    for l in lines:
        segment = l.split()
        segment_name = segment[0]
        onset = float(0)
        offset = float(segment[3]) - float(segment[2])
        speaker = utt2spk[segment_name]
        segment_text = [w for w in word_tokenize(text[segment_name].lower()) if w not in functionwords]
        if speaker in speaker_dict.keys():
            speaker_dict[speaker].append([segment_name, onset, offset, speaker, segment_text])
        else:
            speaker_dict[speaker] = [[segment_name, onset, offset, speaker, segment_text]]
                
    with codecs.open(output_file, mode='w', encoding='UTF-8') as out:
        out.write(item_header)
        for speaker in speaker_dict.keys():
            utts=speaker_dict[speaker]
            if len(utts)<sample_size:
                print('Not enough utterances to sample for speaker: '+speaker)
                next
            elif not rejection:
                utt_ind = np.random.choice(len(utts), sample_size, replace = False)
                for ind in utt_ind:
                    to_write = [utts[ind][0], utts[ind][1], utts[ind][2], utts[ind][3]]
                    out.write(u" ".join([str(e) for e in to_write]) + u"\n")
            else:
                raise AssertionError('Rejection sampling not implemented')
                
    print('done')
            
# Testing
# root = 'D:\\files\\research\\projects\\lf\ivector\\test'
# segments_file = 'segments.txt'
# text_file = 'text.txt'
# utt2spk_file = 'utt2spk.txt'
# output_file = 'test.item'
# generate_utterance_item(root, segments_file, text_file, utt2spk_file, 
#                            output_file)


input_folder = '/fs/clip-realspeech/corpora/spock-format/' + corpus + '/' + matched + '_matched_data_train/'
output_folder = '/fs/clip-realspeech/projects/lfe/eval/utt_abx/items/'
if rejection:
    rejection_name = 'rej'
else:
    rejection_name = 'norej'
output_file = corpus + '_sample'+sample+'_'+rejection_name+'.item
segments_file = 'segments.txt'
text_file = 'text.txt'
utt2spk_file = 'utt2spk.txt'

generate_utterance_item(input_folder, segments_file, text_file, utt2spk_file, 
                            output_folder, output_file, sample_size, rejection):

    

    
    item_file=root+corpus+'.item'

    out_file = root + corpus + '_threshold_' + str(lower_threshold) + '_' + str(upper_threshold) + '.item'
    columns = ['phone', 'prev-phone', 'next-phone', 'speaker']  # ['phone', 'talker']
    print "****"+item_file
    threshold_item(item_file, out_file, columns,
                 lower_threshold=lower_threshold,
                 upper_threshold=upper_threshold)

'''
