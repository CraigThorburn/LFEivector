# -*- coding: utf-8 -*-
# Copyright 2019 Craig Thorburn

"""
Created on Mon May 6 15:05:00 2019
@author: Craig Thorburn
"""
## PARAMETERS
train_corpus = 'WSJ'
test_corpus='WSJ'
matched = 'GPJ'

'''

      - feature_file: string indicating the path to the file where the features will be stored
      - utts: list of utterances id (as specified in 'segments.txt')
      - times: list of numpy arrays containing for each utterance a 1-d numpy array of size nf(utt) the number of feature frames for that utterance, containing timestamps in seconds, given relative to the beginning of the utterance (as specified in 'segments.txt')
      - feats: list of numpy arrays containing for each utterance a 2-d numpy array of size nf(utt) x d, where d is the dimension of the features space, containing the features for each frame of the utterance.

      (The order of utterances and frames should match across all lists and arrays. Frames should be given in increasing order of the timestamps)

'''

      
      

# CODE
import h5features as h5f
import codecs
import os
import numpy as np

def generate_utterance_item(input_folder, output_name, utt2spk_file = None, 
                            include_matlab = False):
    """
    """
    os.chdir(input_folder)    
    ark_filenames = []
    for filename in os.listdir():
        if filename.endswith(".ark") and filename.startswith("ivector"): 
            ark_filenames.append(filename)         

    print(str(len(ark_filenames))+' ivector .ark files found.')
    
    utts=[]
    times=[]
    feats=[]
    for f in ark_filenames:
        print('loading '+f)
        
        with codecs.open(f, mode='r', encoding='UTF-8') as inp:
            lines = inp.read().splitlines()
            for l in lines:
                u = l.strip().split(None, 1)
                vector = u[1].split()
                utts.append(u[0])
                assert(vector.pop(0)=='['),'start of vector marker not found'
                assert(vector.pop(-1)==']'),'end of vector marker not found'
                feats.append(np.array([vector]).astype('float'))
                times.append(np.array([0.1]))   
                print
    with h5f.Writer(output_name) as writer:   
        data = h5f.Data(utts, times, feats, check=True)
        writer.write(data, 'features')

#Test Params
#input_folder = '/mnt/d/files/research/projects/lf/ivector/data'
#output_name = 'test'

input_folder = ('/fs/clip-realspeech/projects/lfe/models/ivector/'+ train_corpus +
    + '/train_and_decode/exp/ivectors_test_'+test_corpus+'WSJ'   )     
output_name = train_corpus+'_'+test_corpus+'.ivector'

generate_utterance_item(input_folder, output_name+'.ivector')