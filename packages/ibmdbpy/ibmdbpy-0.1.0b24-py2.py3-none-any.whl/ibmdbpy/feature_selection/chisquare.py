# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:31:52 2015

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
def chisquare(idadf, target = None, features = None):
    """
    chisquare as defined in 
    A Comparative Study on Feature Selection and Classification Methods Using 
    Gene Expression Profiles and Proteomic Patterns. (GIW02F006)
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    chisquare_dict = dict()
    length = len(idadf)
    
    if target is not None:
        count = idadf.count_groupby(target)
        count_serie = count["count"]
        count_serie.index = count[target]
        C = dict(count_serie)
        
        for feature in features:
            if idadf.indexer == feature:
                # This is useless and expensive to compute the chisquare with a primary key
                chisquare_dict[feature] = np.nan
            else:
                count = idadf.count_groupby(feature)
                count_serie = count["count"]
                count_serie.index = count[feature]
                R = dict(count_serie)
                
                count = idadf.count_groupby([feature , target])
                
                chisquare = 0            
                for target_class in C.keys():
                    count_target = count[count[target] == target_class][[feature, "count"]]
                    A_target = count_target['count']
                    A_target.index = count_target[feature]
                    
                    for feature_class in A_target.index:
                        a = A_target[feature_class]
                        e = R[feature_class] * C[target_class] / length
                        chisquare += ((a - e)**2)/e
                
                chisquare_dict[feature] = chisquare
                    
        # Output
        if len(features) > 1:
            result = pd.Series(chisquare_dict)
            result.sort(ascending = False) 
        else:
            result = chisquare_dict[features[0]]
    else:
        raise NotImplementedError("TODO")
        
    return result
    
@idadf_state
@timed
def chisquare_sql(idadf, target = None, features = None):
    """
    chisquare as defined in 
    A Comparative Study on Feature Selection and Classification Methods Using 
    Gene Expression Profiles and Proteomic Patterns. (GIW02F006)
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    chisquare_dict = dict()
    length = len(idadf)
    
    if target is not None:
        for feature in features:

#SELECT SUM(POWER(a-e,2)/e) FROM (
#SELECT a."dAge",a."dIndustry", COUNT(*) AS a, (count1*count2)/2458285 as e FROM DB2INST1.USCENSUS AS a 
#INNER JOIN
#(SELECT "dAge", COUNT(*) AS count1 FROM DB2INST1.USCENSUS GROUP BY "dAge") AS b ON a."dAge" = b."dAge"
#INNER JOIN 
#(SELECT "dIndustry", COUNT(*) AS count2 FROM DB2INST1.USCENSUS GROUP BY "dIndustry") AS c ON a."dIndustry" = c."dIndustry"
#GROUP BY a."dIndustry",a."dAge", count1, count2)
            if idadf.indexer == feature:
                # This is useless and expensive to compute the chisquare with a primary key
                chisquare_dict[feature] = np.nan
            else:
                joinquery1 = "(SELECT \"%s\", COUNT(*) AS count1 FROM %s GROUP BY \"%s\")"%(target, idadf.name, target)
                joinquery2 = "(SELECT \"%s\", COUNT(*) AS count2 FROM %s GROUP BY \"%s\")"%(feature, idadf.name, feature)
                main = "SELECT SUM(POWER(a-e,2)/e) FROM (SELECT a.\"%s\",a.\"%s\", COUNT(*) AS a, CAST((count1*count2) AS FLOAT)/%s as e FROM %s AS a"%(target, feature, length, idadf.name)
                
                join = "%s INNER JOIN (%s) AS b ON a.\"%s\" = b.\"%s\" INNER JOIN (%s) AS c ON a.\"%s\" = c.\"%s\""%(main, joinquery1, target, target, joinquery2, feature, feature)
                groupby = "GROUP BY a.\"%s\",a.\"%s\", count1, count2)"%(target, feature)
                
                query = "%s %s"%(join, groupby)
                    
                chisquare_dict[feature] = idadf.ida_scalar_query(query)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(chisquare_dict)
            result.sort(ascending = False) 
        else:
            result = chisquare_dict[features[0]]
    else:
        raise NotImplementedError("TODO")
        
    return result
    
    
