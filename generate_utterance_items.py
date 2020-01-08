# -*- coding: utf-8 -*-
# Copyright 2019 Craig Thorburn

"""
Created on Mon May 6 15:05:00 2019
@author: Craig Thorburn
"""
## PARAMETERS
corpus = 'CGN_spoken'
matched = 'CSJ'
min_length = 3
max_length = 100
allowed_overlap = 20
max_attempts = 1
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
                            output_folder, output_file, allowed_overlap, sample_size = 12, rejection = True,
                            max_attempts = 100):
    """
    """
    os.chdir(input_folder)
    item_header = '#file onset offset #speaker\n'
    
    with codecs.open(text_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    text={}
    for l in lines:
        t = l.split(None, 1)
        text[t[0]] = t[1]
    print('text file loaded')

    with codecs.open(utt2spk_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    utt2spk={}
    for l in lines:
        u = l.split(None, 1)
        utt2spk[u[0]] = u[1]
    print('utt2spk file loaded')
                
    with codecs.open(segments_file, mode='r', encoding='UTF-8') as inp:
        lines = inp.read().splitlines()
    print('segments file loaded')
    speaker_dict = {} 
    
    for l in lines:
        segment = l.split()
        segment_name = segment[0]
        onset = float(0)
        offset = float(segment[3]) - float(segment[2])
        if offset < min_length:
            continue
        elif offset > max_length:
            continue
        speaker = utt2spk[segment_name]
        segment_text = [w for w in word_tokenize(text[segment_name].lower()) if w not in functionwords]
        if speaker in speaker_dict.keys():
            speaker_dict[speaker].append([segment_name, onset, offset, speaker, segment_text])
        else:
            speaker_dict[speaker] = [[segment_name, onset, offset, speaker, segment_text]]
    
    print('segments parsed')
    with codecs.open(output_folder+output_file, mode='w', encoding='UTF-8') as out:
        err=0
        out.write(item_header)
        overlap_total = 0
        for speaker in speaker_dict.keys():
            utts=speaker_dict[speaker]
            if len(utts)<sample_size:
                print('Not enough utterances to sample for speaker '+speaker)
                err+=1
                next
            elif not rejection:
                utt_ind = np.random.choice(len(utts), sample_size, replace = False)
                for ind in utt_ind:
                    to_write = [utts[ind][0], utts[ind][1], utts[ind][2], utts[ind][3]]
                    out.write(u" ".join([str(e) for e in to_write]) + u"\n")
            else:
                if len(utts)<sample_size*1.5:
                    print('Warning, few utterances for speaker '+speaker+
                          '. May not be able to sample.')
                sampling_succesful = False
                samples_attempted = 0
                while not sampling_succesful:
                    utt_ind = np.random.choice(len(utts), sample_size, replace = False)
                    full_text = []
                    for ind in utt_ind:
                        full_text += utts[ind][4]
                    print(full_text)
                    print(len(full_text))
                    print(len(set(full_text)))
                    overlap = len(full_text)-len(set(full_text))
                    if overlap < allowed_overlap:
                        sampling_succesful = True
                        overlap_total+=overlap
                        print('Sampling successful for speaker '+speaker+' after '+
                              str(samples_attempted)+' attempts.  Overlap is '+str(overlap))
                        for ind in utt_ind:
                            to_write = [utts[ind][0], utts[ind][1], utts[ind][2], utts[ind][3]]
                            out.write(u" ".join([str(e) for e in to_write]) + u"\n")                       
                    elif samples_attempted < max_attempts:
                        samples_attempted += 1
                    else:
                        print('Sampling failed for speaker '+speaker+' after '+
                              str(samples_attempted)+' attempts.')
                        err+=1
                        break
                
                
    print('total '+str(len(speaker_dict.keys()))+' speakers for corpus')   
    if err > 0:
          print(str(err)+' speakers failed')
    if rejection:
        print('average overlap is '+str(float(overlap_total)/(len(speaker_dict.keys())-err)))
    print('done')
            
# Testing
# root = 'D:\\files\\research\\projects\\lf\ivector\\test'
# segments_file = 'segments.txt'
# text_file = 'text.txt'
# utt2spk_file = 'utt2spk.txt'
# output_file = 'test.item'
# generate_utterance_item(root, segments_file, text_file, utt2spk_file, 
#                            output_file)


input_folder = '/fs/clip-realspeech/corpora/CGN/data/o_ort/test_join_4'
output_folder = '/fs/clip-realspeech/projects/lfe/eval/utt_abx/items/'
if rejection:
    rejection_name = 'rej'
else:
    rejection_name = 'norej'
output_file = corpus + '_sample'+str(sample_size)+'_'+rejection_name+'_min'+str(min_length)+'_max'+str(max_length)+'.item'
segments_file = 'segments'
text_file = 'text'
utt2spk_file = 'utt2spk'

generate_utterance_item(input_folder, segments_file, text_file, utt2spk_file, 
                            output_folder, output_file, 
                        allowed_overlap, sample_size, rejection, max_attempts, )


