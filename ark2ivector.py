# -*- coding: utf-8 -*-
# Copyright 2019 Craig Thorburn

"""
Created on Mon May 6 15:05:00 2019
@author: Craig Thorburn
"""
## PARAMETERS
train_corpus = 'CGN_spoken'
test_corpus='CGN_spoken'
include_ivector = True
include_matlab = False


'''

      - feature_file: string indicating the path to the file where the features will be stored
      - utts: list of utterances id (as specified in 'segments.txt')
      - times: list of numpy arrays containing for each utterance a 1-d numpy array of size nf(utt) the number of feature frames for that utterance, containing timestamps in seconds, given relative to the beginning of the utterance (as specified in 'segments.txt')
      - feats: list of numpy arrays containing for each utterance a 2-d numpy array of size nf(utt) x d, where d is the dimension of the features space, containing the features for each frame of the utterance.

      (The order of utterances and frames should match across all lists and arrays. Frames should be given in increasing order of the timestamps)

	Run as: python [input folder] [output name] [include ivector] [include matlab] [OPTIONAL: utt2spk file]")
	input folder: location of input ark folder
	output name: path to and name of output file
	include ivector: whether to save ivector file
	include matlab: whether to include matlab file
	utt2spk: optional if including matlab - location of utt2spk file
    		

'''

      
      

# CODE
import h5features as h5f
import codecs
import os
import sys
import numpy as np
import scipy.io as sio

def generate_utterance_item(input_folder, output_name, include_ivector = True, utt2spk_file = None, 
                            include_matlab = False):
    """
    """
    os.chdir(input_folder)    
    ark_filenames = []
    for filename in os.listdir('.'):
        if filename.endswith(".ark") and filename.startswith("ivector"): 
            ark_filenames.append(filename)         

    print(str(len(ark_filenames))+' ivector .ark files found.')
    utt2spk_file=None
    if utt2spk_file != None:
        with codecs.open(utt2spk_file, mode='r', encoding='UTF-8') as inp:
            lines = inp.read().splitlines()
        utt2spk={}
        for l in lines:
            u = l.split(None, 1)
            utt2spk[u[0]] = u[1]
        print('utt2spk file loaded')    

    utts=[]
    times=[]
    feats=[]
    spks=[]
    for f in ark_filenames:
        print('loading '+f)
        
        with codecs.open(f, mode='r', encoding='UTF-8') as inp:
            lines = inp.read().splitlines()
            for l in lines:
                u = l.strip().split(None, 1)
                vector = u[1].split()
                utts.append(u[0])
                if utt2spk_file != None:
                    spks.append(utt2spk[u[0]])
                assert(vector.pop(0)=='['),'start of vector marker not found'
                assert(vector.pop(-1)==']'),'end of vector marker not found'
                feats.append(np.array([vector]).astype('float'))
                times.append(np.array([0.1]))   

    if include_ivector:
        with h5f.Writer(output_name+'_vectors.ivector') as writer:   
            data = h5f.Data(utts, times, feats, check=True)
            writer.write(data, 'features')

    if include_matlab:
        sio.savemat(output_name+'_vectors.mat', {output_name+'_vectors':feats, output_name+'_utts':utts, 
            output_name+'_spks':spks})

if len(sys.argv) <= 4:
    print('incorrect arguments')
    print("Run as: python [input folder] [output name] [include ivector] [include matlab] [OPTIONAL: utt2spk file]")
    print(len(sys.argv))
    raise AssertionError

input_folder = sys.argv[1]
output_name = sys.argv[2]
include_ivector = bool(sys.argv[3])
include_matlab = bool(sys.argv[4])


#if include_matlab:
#	utt2spk_file = sys.argv[5]
utt2spk_file=''

#Test Params
#input_folder = '/mnt/d/files/research/projects/lf/ivector/data'
#output_name = 'test'

#input_folder = '/fs/clip-realspeech/projects/lfe/models/ivector/'+ train_corpus + '/train_and_decode/exp/ivectors_join_4_test_join_4_'+test_corpus
#utt2spk_file = '/fs/clip-realspeech/projects/lfe/models/ivector/' + test_corpus + '/train_and_decode/data/test/utt2spk' 
#output_name = train_corpus+'_'+test_corpus

generate_utterance_item(input_folder, output_name, include_ivector, utt2spk_file, include_matlab)