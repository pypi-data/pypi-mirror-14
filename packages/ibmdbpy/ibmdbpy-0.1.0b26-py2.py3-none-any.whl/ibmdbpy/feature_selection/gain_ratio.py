# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:48:18 2015

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
def gain_ratio(idadf, target = None, features = None):
    """
    symmetric information gain ratio [Lopez de Mantaras 1991]
    ---> the rest is not symmetrical 
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    entropy_dict = dict()
    length = len(idadf)
    
    if target is not None:
        value_dict = OrderedDict()
        
        entropy_dict[target] = entropy(idadf, target, mode = "raw")
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy(idadf, feature, mode = "raw")
            join_entropy = entropy(idadf, [target] + [feature], mode = "raw")
            disjoin_entropy = entropy_dict[feature] + entropy_dict[target]
            info_gain = (disjoin_entropy - join_entropy)
            corrector = length*np.log(length)
            value_dict[feature] = (info_gain + corrector)/(join_entropy + corrector)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(value_dict)
            result.sort(ascending = False) 
        else:
            result = value_dict[feature[0]]
    else:
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]     
        
        ### Compute
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] = entropy(idadf, column_pair[0], mode = "raw")
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] = entropy(idadf, column_pair[1], mode = "raw")
            join_entropy = entropy(idadf,  [column_pair[0]] + [column_pair[1]], mode = "raw")     
            disjoin_entropy = entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]]
            info_gain = (disjoin_entropy - join_entropy)
            corrector = length*np.log(length)
            values.append((info_gain + corrector)/(join_entropy + corrector))
            
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        
    return result
    
    
@idadf_state
@timed
def gain_ratio_2(idadf, target = None, features = None):
     # Problem : gain ratio is not symmetric. Matrix impementation is not correct 
    # Check input
    if (target is not None)|(features is not None):
        _check_input(idadf, target, features)
        
    if features is None:
        if target is not None:
            features = [x for x in idadf.columns if x != target]
        else:
            features = list(idadf.columns)
            
    if target is not None : # Do not compute the matrix
        ### Get data
        data = idadf.count_groupby(features + [target])    
        
        # Compute
        value_dict = OrderedDict()
        data_entropy = _compute_entropy(data, target=target)
        
        for feature in features: 
            subset_entropy = _compute_entropy(data, target=target, conditional=feature)  
            intr_value = _compute_entropy(data, target=feature)
            
            value_dict[feature] = (data_entropy - subset_entropy)/intr_value
            
        if len(features) > 1:
            result = pd.Series(value_dict) 
        else:
            result = value_dict[0]
    else:
        ### Get data
        data = idadf.count_groupby(features)    
        
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]
    
        entropy_dict = dict()
        
        ### Compute
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] =  _compute_entropy(data, target=column_pair[1])
            subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1])            
            values.append((entropy_dict[column_pair[0]] - subset_entropy)/entropy_dict[column_pair[1]])
        
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
    
    return result
        
        
        
@idadf_state
@timed
def gain_ratio_2_matrix(idadf, features = None):
    # Check input 
    if features is None:
        features = list(idadf.columns)
    else:
        _check_input_for_matrix(idadf, features)
           
    ### Get data
    data = idadf.count_groupby(features)    
    
    values = []
    combinations = [x for x in itertools.combinations(features, 2)]
    columns_set = [{x[0], x[1]} for x in combinations]

    entropy_dict = dict()
    
    ### Compute
    for column_pair in combinations:
        if column_pair[0] not in entropy_dict:
            entropy_dict[column_pair[0]] =  _compute_entropy(idadf, data, target=column_pair[0])
        if column_pair[1] not in entropy_dict:
            entropy_dict[column_pair[1]] =  _compute_entropy(idadf, data, target=column_pair[1])
        subset_entropy = _compute_entropy(idadf, data, target=column_pair[0], conditional=column_pair[1])            
        values.append((entropy_dict[column_pair[0]] - subset_entropy)/entropy_dict[column_pair[1]])
    
    ### Fill the matrix
    result = _fill_matrix(features, columns_set, values, 1.0)
    return result
        
@idadf_state
@timed
def gain_ratio_1(idadf, target, feature_list = None):
     # Problem : gain ratio is not symmetric. Matrix impementation is not correct 
    if feature_list is None:
        feature_list = [x for x in idadf.columns if x != target]
    else:
        if isinstance(feature_list, six.string_types):
            feature_list = [feature_list]
        # make sure the target is not in feature_list
        if target in feature_list:
            feature_list = [x for x in feature_list if x != target]

    #name = idadf.internal_state.current_state

    value_dict = OrderedDict()
    
    data_entropy = entropy(idadf, target)
    
    for feature in feature_list:
        subset_entropy = 0.0
        intr_value = 0.0
        #attr_values = idadf.ida_query("SELECT DISTINCT \"%s\" FROM %s"%(feature, name))
        #attr_values = list(attr_values[feature])
        attr_values = idadf.unique(feature)
        
        #import pdb ; pdb.set_trace()
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            intr_value -= factor*log2(factor)
            subset_entropy += factor*entropy(subset, target)  ### + ??? 
        
        if intr_value != 0:
            info_gain_ratio = (data_entropy - subset_entropy)/intr_value
        else:
            info_gain_ratio = 0
        # what to do if intr_value = 0 ?? (case with dummy variable)
        value_dict[feature] = info_gain_ratio   
        
    if len(feature_list) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return info_gain_ratio