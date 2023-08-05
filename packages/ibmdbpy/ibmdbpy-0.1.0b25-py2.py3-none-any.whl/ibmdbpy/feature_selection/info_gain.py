# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 08:59:00 2015

@author: efouche
"""

from collections import OrderedDict

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

import pandas as pd
from numpy import log2, log

import itertools

import six
#from ibmdbpy.feature_selection import discretize
from ibmdbpy.feature_selection.entropy import entropy

from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix, _check_input, _add_constant


@idadf_state
@timed
def info_gain(idadf, target = None, features = None):
    """
    """
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################
    
    entropy_dict = OrderedDict()  # cache
    length = len(idadf)
    loglength = log(length)
        
    if target is not None : # Do not compute the matrix
            
        target_entropy = entropy(idadf, target, mode = "raw")
        
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy(idadf, feature, mode = "raw")
            join_entropy = entropy(idadf, [target] + [feature],mode = "raw")
            entropy_dict[feature] = ((target_entropy + entropy_dict[feature] - join_entropy)/length + loglength)/log(2)
            
        if len(features) == 1:
            result = entropy_dict[features[0]]
        else:
            result = pd.Series(entropy_dict)
            result.sort(ascending = False)
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
            values.append(((entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]] - join_entropy)/length + loglength)/log(2))
    
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, "X")
            
    return result

@idadf_state
@timed
def info_gain_sql1(idadf, target, features = None):
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################
    
    entropylist = []
    target_entropy = entropy(idadf, target, mode = "raw")
    
    ######################################################
    for feature in features: 
        entropystr = entropy(idadf, feature, mode = "raw", execute = False)
        entropystr = _add_constant(entropystr, feature, "column")
        entropylist.append(entropystr)
    query = " UNION ALL ".join(entropylist)
    
    entropy1 = idadf.ida_query(query)
    entropy1_serie = entropy1['ent']
    entropy1_serie.index = entropy1['column']
    
    #######################################################
    iglist = []
    for feature in features:
        igstr = entropy(idadf, [feature] + [target], mode = "raw", execute = False)
        igstr = _add_constant(igstr, feature, "column")
        iglist.append(igstr)
    query = " UNION ALL ".join(iglist)
    
    ig = idadf.ida_query(query)
    ig_serie = ig['ent']
    ig_serie.index = ig['column']
    
    result = pd.Series()
    for value in ig_serie.index:
        result[value] = (((entropy1_serie[value] + target_entropy - ig_serie[value])/len(idadf)) + log(len(idadf)))/log(2)
    
    result.sort(ascending = False)
    return result
 
@idadf_state
@timed   
def info_gain_sql2(idadf, target, features = None):
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################
    from ibmdbpy.feature_selection.entropy import entropy_4
    entropylist = []
    target_entropy = entropy_4(idadf, target, log2 = False)
    
    ######################################################
    for feature in features: 
        entropystr = entropy_4(idadf, feature, log2 = False, execute = False)
        entropystr = _add_constant(entropystr, feature, "column")
        entropylist.append(entropystr)
    query = " UNION ALL ".join(entropylist)
    
    entropy1 = idadf.ida_query(query)
    entropy1_serie = entropy1['ent']
    entropy1_serie.index = entropy1['column']
    
    #######################################################
    iglist = []
    for feature in features:
        joinstr = entropy_4(idadf, [feature] + [target], log2 = False, execute = False)
        igstr = "SELECT (%s + %s - SUM(-count*LOG(count)))/LOG(2) as ent"%(target_entropy, entropy1_serie[feature]) + joinstr[36:]
        igstr = _add_constant(igstr, feature, "column")
        iglist.append(igstr)
    query = " UNION ALL ".join(iglist)
    query = query + " ORDER BY \"ENT\" DESC"
    
    ig = idadf.ida_query(query)
    ig_serie = ig['ent']
    ig_serie.index = ig['column']
    
    return ig_serie.copy()

def info_gain_python1(idadf, target = None, features = None):   
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################  
       
    if target is None:    
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
            subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1])            
            values.append(entropy_dict[column_pair[0]] - subset_entropy)
    
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, "X")
        return result          
        
    # Get data 
    data = idadf.count_groupby(features + [target])   
        
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features: 
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)  
        value_dict[feature] = data_entropy - subset_entropy
    
    result = pd.Series(value_dict)
    result.sort(ascending = False)
    return result 

@idadf_state
@timed        
def info_gain_python2(idadf, target, features = None):
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################  
    value_dict = OrderedDict()
    
    data_entropy = 0.0
    data = idadf.ida_query("SELECT \"%s\", COUNT(*) FROM %s GROUP BY \"%s\""%(target,idadf.name,target))
    count = data[data.columns[-1]]
    count.index = data[data.columns[0]]
    for value in count:
        info = value / len(idadf)
        data_entropy += ((-info) * log2(info))
    
    for feature in features:
        subset_entropy = 0.0               
        
        data = idadf.ida_query("SELECT \"%s\",  \"%s\", COUNT(*) AS \"count\" FROM %s GROUP BY \"%s\", \"%s\""%(feature,target,idadf.name,feature,target))
        count_1 = data.pivot_table(index = data.columns[0], aggfunc = "sum")['count']
        count_2 = data.pivot_table(index = [data.columns[0], data.columns[1]], aggfunc = "sum")['count']
        
        for value in count_2.index.levels[0]:
            data = count_2[value]
            factor = count_1[value]/len(idadf)
            subentropy = 0.0
            for value_2 in data:
                info = value_2 / count_1[value]
                subentropy += ((-info) * log2(info))
                        
            subset_entropy += factor*subentropy

        value_dict[feature] = data_entropy - subset_entropy
    
    result = pd.Series(value_dict)
    result.sort(ascending = False)
    return result
 
@idadf_state
@timed   
def info_gain_python3(idadf, target, features = None):
    # Check input
    ###########################################################################
    target, features = _check_input(idadf, target, features)
    ###########################################################################  
    
    value_dict = OrderedDict()
    
    data_entropy = entropy(idadf, target)
    
    for feature in features:
        subset_entropy = 0.0
        attr_values = idadf.unique(feature)
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            subset_entropy += factor*entropy(subset, target)
            #print("feature %s : value %s : factor %s : subentropy %s"%(feature, value, factor, subset_entropy))
            
        value_dict[feature] = data_entropy - subset_entropy
    
    result = pd.Series(value_dict)
    result.sort(ascending = False)
    return result

