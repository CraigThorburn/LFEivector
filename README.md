# lfe

This repository contains helper functions for generating ivectors models for testing the Language Familiarity Effect.  While models are created using Kaldi recipe sre08, the files here provide auxiliary functions such as generating items and wrangling initial data

## data_split_join.py
Either split or join segments to form new datset.  Creates entirely new directory within data folder.  Only works if there is only one speaker per file

Run as: 
```
python [base data folder] [input folder] [output folder] ['split' OR 'join' OR 'reduce'] [number]
```
If 'split', number = how many output files should be created from each input
If 'join', number = how many input files should be concatenated to form one output
If 'reduce', number = factor by which to reduced length of each utterance

## generate_task_utt.py

## get_item_stats.py

## threshold_item.py

## ark2ivector.py

## generate_task.py

## generate_utterance items.py

## run_abx.py

## run_utt_abx.py
