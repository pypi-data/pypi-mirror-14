# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:05:39 2015

@author: efouche
"""

from numbers import Number

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed
from collections import OrderedDict


from numpy import log, log2
import pandas as pd

import six


def differential_entropy(idadf, target = None, mode = "normal", execute = True, having = None):
    pass
    # TODO
   
@idadf_state
@timed
def entropy(idadf, target = None, mode = "normal", execute = True):
    if target is not None:
        if isinstance(target, six.string_types):
            target = [target]
            
        targetstr = "\",\"".join(target)
        subquery = "SELECT COUNT(*) AS a FROM %s GROUP BY \"%s\""%(idadf.name,targetstr)
        if mode == "normal":
            length = len(idadf)
            query = "SELECT(SUM(-a*LOG(a))/%s+LOG(%s))/LOG(2)FROM(%s)"%(length, length, subquery)
        elif mode == "raw":
            query = "SELECT SUM(-a*LOG(a)) FROM(%s)"%(subquery)
        
        if not execute:
            return query
        return idadf.ida_scalar_query(query)
    else:
        entropy_dict = OrderedDict()
        for column in idadf.columns:
           entropy_dict[column] = entropy(idadf, column, mode = mode)
                    
        # Output
        if len(idadf.columns) > 1:
            result = pd.Series(entropy_dict)
            result.sort(ascending = False) 
        else:
            result = entropy_dict[idadf.columns[0]]
        return result
        
@idadf_state
@timed
def entropy_mean(idadf, target = None, mode = "normal", execute = True):
    """
    good idea ?
    """
    if target is not None:
        if isinstance(target, six.string_types):
            target = [target]
            
        targetstr = "\",\"".join(target)
        length = len(idadf)
        
        subquery = "SELECT COUNT(*) AS a FROM %s GROUP BY \"%s\""%(idadf.name,targetstr)
        if mode == "normal":
            query = "SELECT(LOG(%s) - LOG(SUM(a*a)/%s))/LOG(2)FROM(%s)"%(length, length, subquery)
        elif mode == "raw":
            query = "SELECT -LOG(SUM(a)/%s)FROM(%s)"%(length, subquery) # second length to delete for efficiency
        
        if not execute:
            return query
        
        return idadf.ida_scalar_query(query)
    else:
        entropy_dict = OrderedDict()
        for column in idadf.columns:
           entropy_dict[column] = entropy_mean(idadf, column, mode = mode)
                    
        # Output
        if len(idadf.columns) > 1:
            result = pd.Series(entropy_dict)
            result.sort(ascending = False) 
        else:
            result = entropy_dict[idadf.columns[0]]
        return result
    
@idadf_state
@timed
def entropy_having(idadf, target = None, mode = "normal", execute = True, having = None):
    if target is not None:
        if isinstance(target, six.string_types):
            target = [target]
            
        targetstr = "\",\"".join(target)
        
        if having:
            subquery = "SELECT COUNT(*) AS count FROM %s GROUP BY \"%s\" HAVING count >= %s"%(idadf.name,targetstr,having)
        else:
            subquery = "SELECT COUNT(*) AS count FROM %s GROUP BY \"%s\""%(idadf.name,targetstr)
        if mode == "normal":
            length = len(idadf)
            query = "SELECT (SUM(-count*LOG(count))/%s + LOG(%s))/LOG(2) as ent FROM (%s)"%(length, length, subquery)
        elif mode == "raw":
            query = "SELECT SUM(-count*LOG(count)) as ent FROM (%s)"%(subquery)
        
        if not execute:
            return query
        
        return idadf.ida_scalar_query(query)
    else:
        entropy_dict = OrderedDict()
        for column in idadf.columns:
           entropy_dict[column] = entropy_having(idadf, column, mode = mode)
                    
        # Output
        if len(idadf.columns) > 1:
            result = pd.Series(entropy_dict)
            result.sort(ascending = False) 
        else:
            result = entropy_dict[idadf.columns[0]]
        return result

@idadf_state
def conditional_entropy(idadf, target, conditional, log2 = True, execute = True):
     # no join (UNION ALL)
    if isinstance(target, six.string_types):
        target = [target]
    if isinstance(conditional, six.string_types):
        conditional = [conditional]
    
    #log2 = True
    log2str = ''
    if log2 is True:
        log2str = "*LOG(2)"
        
    length = len(idadf)
        
    ent1 = entropy(idadf, target + conditional, mode = "raw", execute = False)
    ent2 = entropy(idadf, conditional, mode = "raw", execute = False)
    query = "SELECT (MAX(ent) - MIN(ent))/(%s%s) FROM (%s)"%(length, log2str, " UNION ALL ".join([ent1,ent2]))
    
    if not execute:
        return query    
    
    return idadf.ida_scalar_query(query)
    
@idadf_state
def conditional_entropy_1(idadf, target, conditional, log2 = True, execute = True):
    # with join
    if isinstance(target, six.string_types):
        target = [target]
    if isinstance(conditional, six.string_types):
        conditional = [conditional]
    
    #log2 = True
    log2str = ''
    if log2 is True:
        log2str = "*LOG(2)"
        
    length = len(idadf)
        
    conditionalstr = "\",\"".join(conditional)
    condition = " AND ".join(["A.\"%s\" = B.\"%s\""%(cond,cond) for cond in conditional])
    atarget = ", ".join(["A.\"%s\""%(tar) for tar in target])
    aconditional = ", ".join(["A.\"%s\""%(cond) for cond in conditional if cond not in target])
    groupbystr = ", ".join([atarget , aconditional, "COUNT1"])
    if not aconditional:
        groupbystr = ", ".join([atarget, "COUNT1"])
    subsubquery = "(SELECT \"%s\",CAST(count(*) AS FLOAT) as COUNT1 FROM %s GROUP BY \"%s\")"%(conditionalstr, idadf.name, conditionalstr)
    subquery = ("SELECT B.COUNT1, CAST(count(*) AS FLOAT) as COUNT2 FROM %s AS A "+
                "INNER JOIN (%s) AS B ON %s GROUP BY %s")%(idadf.name, subsubquery, condition, groupbystr)
    query = "SELECT SUM(COUNT2*LOG(COUNT1/COUNT2))/(%s%s) FROM (%s)"%(length, log2str, subquery)
  
    if not execute:
        return query    
    
    return idadf.ida_scalar_query(query)  
    
    
@idadf_state
@timed
def entropy_4(idadf, target = None, log2 = True, execute = True):
    # Normal log2 entropy calculation 
    # Maybe need more computing in the database
    if target is not None:
        if isinstance(target, six.string_types):
            target = [target]
            
        log2str = ''
        if log2 is True:
            log2str = "/LOG(2)"
            
        targetstr = "\",\"".join(target)
        length = len(idadf)
        
        subquery = "SELECT CAST(COUNT(*) AS FLOAT)/%s AS count FROM %s GROUP BY \"%s\""%(length, idadf.name,targetstr)
        query = "SELECT SUM(-count*LOG(count))%s as ent FROM (%s)"%(log2str, subquery)
    
        if execute is False:
            return query
        return idadf.ida_scalar_query(query)
    else:
        entropy_dict = OrderedDict()
        for column in idadf.columns:
           entropy_dict[column] = entropy_4(idadf, column)
                    
        # Output
        if len(idadf.columns) > 1:
            result = pd.Series(entropy_dict)
            result.sort(ascending = False) 
        else:
            result = entropy_dict[idadf.columns[0]]
        return result
    
    
@idadf_state
def entropy_3(idadf, target):
    data_entropy = 0.0
    count = idadf.ida_query("SELECT COUNT(*) FROM %s GROUP BY \"%s\""%(idadf.name,target))

    for value in count:
        info = value / len(idadf)
        data_entropy += ((-info) * log2(info))
    
    return data_entropy 
    
def entropy_2(idadf, target):
    target_values = idadf.unique(target)
    
    data_entropy = 0.0
    
    for value in target_values:
        freq = len(idadf[idadf[target] == value])
        info = freq / len(idadf)
        if info != 0: # important, otherwise may have nan 
            data_entropy += ((-info) * log2(info))
    
    return data_entropy    

#@idadf_state        
def entropy_1(idadf, target, disc = None):
    if isinstance(target, list):
        target = target[0]
    
    if disc is not None:
        bins = 10
        numerical_columns = idadf._get_numerical_columns()
        level_ratio = idadf.levels(target)/len(idadf)
        if (target in numerical_columns) & (level_ratio > 0.05): # arbitrary
            mini = idadf[target].min()
            maxi = idadf[target].max()   #### Problem 
            interval = (maxi - mini) / bins
            #import pdb; pdb.set_trace()
            target_values = [(mini+interval*x, mini+interval*(x+1)) for x in range(0,10)]
        else:
            target_values = idadf.unique(target)
    else:
        target_values = idadf.unique(target)
    
    data_entropy = 0.0
    
    for value in target_values:
        if isinstance(value, tuple):
            if value == target_values[0]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
            elif value == target_values[-1]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] <= value[1])])
            else:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
        else: 
        
            freq = len(idadf[idadf[target] == value])
        
        info = freq / len(idadf)
        
        if info != 0: # important, otherwise may have nan 
            data_entropy += ((-info) * log2(info))
    
    return data_entropy
    
@idadf_state   
def information_entropy_split(idadf, feature, cut, target):
    """
    SQL Pushdown computing of class information entropy of the partition of
    attribute <feature> w.r.t to cut point <cut> and target <target>
    """
    #if not isinstance(idadf, ibmdbpy.frame.IdaDataFrame):
     #   raise TypeError("idadf is not an IdaDataFrame")
    if not isinstance(feature, six.string_types):
        raise TypeError("feature is not of string type")
    if not feature in idadf:
        raise ValueError("feature does not exists in idadf")
    if not feature in idadf._get_numerical_columns():
        raise ValueError("feature does not belong to numerical attributes of idadf")
    
    if not isinstance(cut, Number):
        raise("The cut-value is not a number")
    
    if not target in idadf:
        raise ValueError("target does not exists in idadf")
    
    idadf_1 = idadf[idadf[feature] <= cut]#[[feature, target]]
    idadf_2 = idadf[idadf[feature] > cut]#[[feature, target]]
    
    if (len(idadf_1) in [0,len(idadf)]):
        feature = idadf[feature]
        raise ValueError("Invalid value for cut-value, because %s attribute range from %s to %s"
                         %(feature, feature.min(), feature.max()))
        
    entropy_1 = entropy(idadf_1, target)
    entropy_2 = entropy(idadf_2, target)
            
    return (len(idadf_1)/len(idadf))*entropy_1 + (len(idadf_2)/len(idadf))*entropy_2
