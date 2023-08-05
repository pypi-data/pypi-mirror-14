# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:46:25 2015

@author: efouche
"""

from numbers import Number

from numpy import log2
import pandas as pd

import six
#from ibmdbpy.utils import timed

def _compute_entropy(count_groupby, target, conditional = None, way = 2):
    if isinstance(target, six.string_types):
        target = [target]
        
    nrecord = count_groupby['count'].sum()
    #if not isinstance(len_idadf, Number):
    #    raise TypeError("len_idadf should be a number")
    entropy = 0.0
    if conditional is None:
        target_count = count_groupby.pivot_table(index = target, aggfunc = "sum")['count']

        for value in target_count:
            #info = value / len_idadf
            info = value / nrecord
            entropy += ((-info) * log2(info))
    else:
        cond_feature_count = count_groupby.pivot_table(index = [conditional] + target, aggfunc = "sum")['count']
        
        for value in cond_feature_count.index.values:
            pxy = cond_feature_count[value[0]][value[1]]/nrecord
            px = cond_feature_count[value[0]].sum()/nrecord
            entropy += ((pxy)*log2(px/pxy))
     
    return entropy
    
def _compute_entropy_old(len_idadf, count_groupby, target, conditional = None):
    if not isinstance(len_idadf, Number):
        raise TypeError("len_idadf should be a number")
    entropy = 0.0
    if conditional is None:
        target_count = count_groupby.pivot_table(index = target, aggfunc = "sum")['count']

        for value in target_count:
            info = value / len_idadf
            entropy += ((-info) * log2(info))
    else:
        #feature_count = count_groupby.pivot_table(index = conditional, aggfunc = "sum")['count']
        cond_feature_count = count_groupby.pivot_table(index = [conditional, target], aggfunc = "sum")['count']
        
        for value in cond_feature_count.index.levels[0]:
            cond_count = cond_feature_count[value]
            #factor = feature_count[value]/len_idadf
            factor = cond_count.sum() / len_idadf
            subentropy = 0.0
            for val in cond_count:
                #info = val / feature_count[value]
                info = val / cond_count.sum()
                subentropy += ((-info) * log2(info))
                
            entropy += factor*subentropy
            
    return entropy

def _fill_matrix(features, columns_set, values, fill_middle):
    tuple_list = []
    for column1 in features:
        list_value = []
        for column2 in features:
            if column1 == column2:
                list_value.append(fill_middle)
            else:
                for index, column_set in enumerate(columns_set):
                    if {column1, column2} == column_set:
                        list_value.append(values[index])
                        break
        tuple_list.append(tuple(list_value))

    result = pd.DataFrame(tuple_list)
    result.index = features
    result.columns = features
    return result
    
def _add_constant(selectstr, constant, asclause):
    asclause = 'as %s'%asclause
    return "SELECT '%s' %s,"%(constant, asclause) + selectstr[6:]

def _check_input(idadf, target, features):
    """
    Check if the input is valid. 
    """
    if target is not None:
        if not isinstance(target, six.string_types):
            raise ValueError("target should be a string")
        if target not in idadf.columns:
            raise ValueError("Unknown column %s"%target)
    
    if features is not None:
        if isinstance(features, six.string_types):
            if features not in idadf.columns:
                raise ValueError("Unknown column %s"%features)
            features = [features]
        for x in features:
            if x not in idadf.columns:
                raise ValueError("Unknown column %s"%x)
    else:
        if target is not None:
            features = [x for x in idadf.columns if x not in target]
        else:
            features = list(idadf.columns)
            
    return target, features

#def _check_input(idadf, target = None, features = None):   
#    if features is not None:
#        if not isinstance(features, six.string_types)|isinstance(features, list):
#            raise TypeError("Feature is not a string or a list of strings")
#        if isinstance(features, six.string_types):
#            features = [features]
#        unknown_features = []
#        for feature in features:
#            if feature not in idadf.columns:
#                unknown_features.append("%s"%feature)
#        if unknown_features:
#            raise ValueError("Unknown columns: %s"%", ".join(unknown_features))
#            
#    if target is not None:
#        if not isinstance(target, six.string_types):
#            raise TypeError("Target not a string")
#        if target not in idadf.columns:
#            raise ValueError("Unknown target column : %s"%target)
#        if features is not None:
#            if target in features:
#                raise ValueError("Target in features")
            
def _check_input_for_matrix(idadf, features):
    if isinstance(features, six.string_types) | (len(features) == 1):
        raise ValueError("A list of features (at least 2) is needed to compute the matrix")
    unknown_features = []
    for feature in features:
        if feature not in idadf.columns:
            unknown_features.append("%s"%feature)
    if unknown_features:
        raise ValueError("Unknown columns: %s"%", ".join(unknown_features))
        
        