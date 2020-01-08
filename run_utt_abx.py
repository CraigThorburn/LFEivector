# -*- coding: utf-8 -*-
"""
Created on Wed May 7 14:28:04 2019

@author: Thomas Schatz

Compute distances, scores and results given task and features
with simple Euclidean distance

Usage: 
    python run_abx.py feat_file task_file res_folder res_id
"""


# change to distance to force choice of normalization is crazy and crazily done
# this should not affect the ABXpy code in the slightest...
# the name of the optional argument is even forced!!!

import ABXpy.distances.distances as dis
import ABXpy.score as sco
import ABXpy.analyze as ana
import numpy as np
import scipy.spatial.distance


def run_ABX(feat_file, task_file, dis_file, score_file, result_file, distance, normalized):
    """
    Run distances, scores and results ABXpy steps based on
    provided features and task files.
    Results are saved in:
        $res_folder/distances/'$res_id'.distances
        $res_folder/scores/'$res_id'.scores
        $res_folder/results/'$res_id'.txt
    """
    dis.compute_distances(feat_file, '/features/', task_file, dis_file,
                          distance, normalized=normalized, n_cpu=1)
    sco.score(task_file, dis_file, score_file)
    ana.analyze(task_file, score_file, result_file)


if __name__=='__main__':
    import argparse
    import os.path as path
    parser = argparse.ArgumentParser()
    parser.add_argument('feat_file', help='h5features file')
    parser.add_argument('task_file', help='ABXpy task file')
    parser.add_argument('res_folder', help=('Result folder (must contain'
                                            'distances, scores and results'
                                            'subfolders)'))
    parser.add_argument('res_id', help=('identifier for the results'
                                        '(model + task)'))
    args = parser.parse_args()
    assert path.exists(args.feat_file), ("No such file "
                                         "{}".format(args.feat_file))
    assert path.exists(args.task_file), ("No such file "
                                         "{}".format(args.task_file))
    dis_file = path.join(args.res_folder, 'distances',
                         args.res_id + '.distances')    
    score_file = path.join(args.res_folder, 'scores',
                           args.res_id + '.scores')
    result_file = path.join(args.res_folder, 'results',
                            args.res_id + '.txt')
    assert not(path.exists(dis_file)), \
        "{} already exists".format(dis_file)
    assert not(path.exists(score_file)), \
        "{} already exists".format(score_file)
    assert not(path.exists(result_file)), \
        "{} already exists".format(result_file)
    distance = lambda x, y, normalized: scipy.spatial.distance.cdist(x, y, 'euclidean')
    run_ABX(args.feat_file, args.task_file, dis_file, score_file, result_file,
            distance, normalized=True)
