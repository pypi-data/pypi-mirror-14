# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:29:30 2015

@author: efouche
"""


from collections import OrderedDict

#import itertools 

#from ibmdbpy.feature_selection.entropy import entropy 

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

#from numpy import log2
import pandas as pd

import six


#from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix
from ibmdbpy.feature_selection.private import _check_input

@idadf_state
@timed
def gini(idadf, features = None):
        
    if features is None:
        features = list(idadf.columns)
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, features = features)
      
        
    value_dict = OrderedDict()
        
    length = len(idadf)**2
    
    for feature in features: 
        
        subquery = "SELECT COUNT(*) AS count FROM %s GROUP BY \"%s\""%(idadf.name, feature)
        query = "SELECT (%s - SUM(POWER(count,2)))/%s FROM (%s)"%(length, length, subquery)
        value_dict[feature] = idadf.ida_scalar_query(query)
            
        if len(features) > 1:
            result = pd.Series(value_dict) 
        else:
            result = value_dict[feature]
    
    return result

@idadf_state
@timed
def gini_2(idadf, features = None):
        
    if features is None:
        features = list(idadf.columns)
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, features = features)
      
        
    value_dict = OrderedDict()
        
    for feature in features:  
        subquery = "SELECT CAST(COUNT(*) AS FLOAT)/%s AS count FROM %s GROUP BY \"%s\""%(len(idadf),idadf.name, feature)
        query = "SELECT 1 - SUM(POWER(count,2)) FROM (%s)"%subquery
        value_dict[feature] = idadf.ida_scalar_query(query)
            
        if len(features) > 1:
            result = pd.Series(value_dict) 
        else:
            result = value_dict[feature]
    
    return result
    
@idadf_state
@timed
def gini_1(idadf, features = None):
        
    if features is None:
        features = list(idadf.columns)
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, features = features)
      
    data = idadf.count_groupby(features)
    nrecords = data['count'].sum()
        
    value_dict = OrderedDict()
        
    for feature in features: 
        class_count = data.pivot_table(index = feature, aggfunc = "sum")['count']
        value_dict[feature] = 1 - sum([(x/nrecords)**2 for x in class_count])
            
        if len(features) > 1:
            result = pd.Series(value_dict) 
        else:
            result = value_dict[feature]
    
    return result
    
    
    