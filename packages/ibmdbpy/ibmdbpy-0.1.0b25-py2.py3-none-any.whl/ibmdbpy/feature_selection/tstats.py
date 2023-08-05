# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:05:27 2015

@author: efouche
"""

from collections import OrderedDict

import itertools 

from ibmdbpy.feature_selection.entropy import entropy 

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

from numpy import log2
import numpy as np 
import pandas as pd

import six


from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix
from ibmdbpy.feature_selection.private import _check_input, _check_input_for_matrix


@idadf_state
@timed
def ttest(idadf, target = None, features = None):
    """
    Modified ttest as defined in 
    A Modified T-test feature Selection Method and Its Application on
    the HapMap Genotype Data
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    ttest_dict = dict()
    length = len(idadf)
    
    ## quick fix, avoid having the indexer
    features = [x for x in features if x != idadf.indexer]
    
    if target is not None:
       
        count = idadf.count_groupby(target)
        target_count = count["count"]
        target_count.index = count[target]
        M = np.sqrt(1/target_count + 1/length)        
        S = idadf.within_class_std(target = target, features = features)
        #S0 = S.median()
        class_mean = idadf.mean_groupby(target, features = features)
        mean = idadf.mean()
        
        print(M)
        print(S)
        
        for feature in features:
            ttest_dict[feature] = dict()
            for target_class in class_mean.index:
                numerator = class_mean.loc[target_class][feature] - mean[feature]
                denominator = M[target_class] * S[feature]
                
                ttest_dict[feature][target_class] = numerator / denominator
                    
        for feature in features:
            ttest_dict[feature] = max(ttest_dict[feature].values())
            
        # Output
        if len(features) > 1:
            result = pd.Series(ttest_dict)
            result.sort(ascending = False) 
        else:
            result = ttest_dict[features[0]]
    else:
        raise NotImplementedError("TODO")
        
    return result