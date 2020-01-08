# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:45:01 2019

@author: craig
"""
# THIS ONLY WORKS IF THERE IS ONLY ONE SPEAKER PER FILE
# Run as: python [base data folder] [input folder] [output folder] ['split' OR 'join'] [number]
# If 'split', number = how many output files should be created from each input
# If 'join', number = how many input files should be concatenated to form one output

import os
import codecs
import sys
from shutil import copyfile

if len(sys.argv) !=6:
    print('incorrect arguments')
    print("Run as: python [base data folder] [input folder] [output folder] ['split' OR 'join'] [number]")
    print(len(sys.argv))
    raise AssertionError
root = sys.argv[1]
input_folder = sys.argv[2]
output_folder = sys.argv[3]
split_join = sys.argv[4]
split_join_num = int(sys.argv[5])



os.chdir(root+'/'+input_folder)


parsed_text={}
parsed_utt2spk = {}


print('parsing text file')
with codecs.open('text', mode = 'r', encoding='UTF-8') as inp:
    lines = inp.read().splitlines()
    for l in lines:
        item = l.split(' ')
        utt_id = item.pop(0)
        text = ' '.join(str(e) for e in item)
        parsed_text[utt_id] = text        
        
print('parsing utt2spk file')        
with open('utt2spk', mode = 'r') as inp:
    train_utt2spk=[]
    test_utt2spk=[]       
    lines = inp.read().splitlines()
    for l in lines:
        utt_id = l.split(' ')[0]
        spk = l.split(' ')[1]
        parsed_utt2spk[utt_id] = spk   

print('parsing and editing segments file')
with open('segments', mode = 'r') as inp:    
    lines = inp.read().splitlines()
    total_utts = len(lines)
    
    new_segments = []
    new_text = []
    new_utt2spk = []
    
    if split_join == 'split':
            print('splitting operation')
            print('warning: text will not be correct for splitting operation')

            for l in lines:
                item = l.split(' ')


                utt_id = item[0]
                record_id = item[1]
                start = float(item[2])           
                end = float(item[3])
                new_utt_length = (end - start)/split_join_num
                for n in range(int(split_join_num)):
                    new_utt_id = item[0] + '_' + str(n)
                    new_record_id = item[1]
                    new_start = start + n*new_utt_length
                    new_end = start + (n+1)*new_utt_length

                    new_segments.append([new_utt_id, new_record_id, str(new_start), str(new_end)])
                    new_utt2spk.append([new_utt_id, parsed_utt2spk[utt_id]])
                    new_text.append([new_utt_id, parsed_text[utt_id]])

    
    elif split_join == 'join':
            print('joining operation')
            item_num = 0
            utt_ids = []
            record_ids=[]
            starts = []
            ends = []
            for l in lines:
                item = l.split(' ')
                if item_num>0:
                    if item[1] != record_ids[-1]:
                        item_num=0
                        utt_ids = []
                        record_ids=[]
                        starts = []
                        ends = []
                        continue

                utt_ids.append(item[0])
                record_ids.append(item[1])
                starts.append(item[2])
                ends.append(item[3])

                item_num+=1
                '''print(item)
                print(utt_ids)
                print(record_ids)
                print(starts)
                print(ends)
                print(item_num)
                a=input()'''
                if item_num==split_join_num:
                    new_utt_id = item[0] + 'j'
                    new_record_id = item[1]
                    new_start = starts[0]
                    new_end = ends[-1]  

                    new_segments.append([new_utt_id, new_record_id, str(new_start), str(new_end)])

                    new_utt2spk.append([new_utt_id, parsed_utt2spk[item[0]]])
                    new_text.append([new_utt_id, ''.join([parsed_text[utt] for utt in utt_ids])])
                    item_num=0
                    utt_ids = []
                    record_ids=[]
                    starts = []
                    ends = []
                
                
new_total_utts = len(new_segments)

if split_join=='join':
    print('joining complete: reduced from '+str(total_utts)+' utterances to '+str(new_total_utts)+' utterances')
elif split_join == 'split':
    print('joining complete: increased from '+str(total_utts)+' utterances to '+str(new_total_utts)+' utterances')
        
os.chdir('../'+output_folder)         
print('saving segments file')            
with open('segments', mode='w') as out:
    for e in new_segments:
        out.write(' '.join([i for i in e]) + u"\n")  


print('saving utt2spk file')            
with open('utt2spk', mode='w') as out:
    for e in new_utt2spk:
        out.write(' '.join([i for i in e]) + u"\n")  
                  

print('saving text file')            
with codecs.open('text', mode='w', encoding='UTF-8') as out:
    for e in new_text:
        out.write(' '.join([i for i in e]) + u"\n")  

print('moving wav.scp file')
copyfile('../'+input_folder+'/'+'wav.scp','wav.scp')
        
print('done')
    