# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:53:19 2015

@author: efouche
"""

from collections import OrderedDict

import ibmdbpy

from ibmdbpy.feature_selection import entropy
from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix
from ibmdbpy.feature_selection.private import _check_input#, _compute_entropy, _add_constant

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

import pandas as pd
import numpy as np

import itertools
import six

@idadf_state
@timed
def outer_su(idadf1, key1, idadf2, key2, target = None, features1 = None, features2 = None):
    """
    """
    target1, features1 = _check_input(idadf1, target, features1)
    target2, features2 = _check_input(idadf2, None, features2)
    
    if key1 not in idadf1.columns:
        raise ValueError("%s is not a column in idadf1")
    if key2 not in idadf2.columns:
        raise ValueError("%s is not a column in idadf2")
       
    condition = "a.\"%s\" = b.\"%s\""%(key1,key2)
    
    afeaturesas = ", ".join(["a.\"%s\" as \"a.%s\" "%(feature, feature) for feature in features1])
    bfeaturesas = ", ".join(["b.\"%s\" as \"b.%s\" "%(feature, feature) for feature in features2])
    
    selectlist = [afeaturesas, bfeaturesas]
    
    if target1 is not None:
        atargetas = ", ".join(["a.\"%s\" as \"a.%s\" "%(tar, tar) for tar in [target1]])
        selectlist.append(atargetas)
        atarget = "a." + target1
    else:
        atarget = None
        
    abfeatures = ["a." + feature for feature in features1] + ["b." + feature for feature in features2]
    selectstr = ", ".join(selectlist)
    
    expression = "SELECT %s FROM %s as a FULL OUTER JOIN %s as b ON %s"%(selectstr, idadf1.name, idadf2.name, condition)
    
    viewname = idadf1._idadb._create_view_from_expression(expression)
    
    try:
        idadf_join = ibmdbpy.IdaDataFrame(idadf1._idadb, viewname)
        return su(idadf_join, target = atarget, features = abfeatures)
    except:
        raise
    finally:
        idadf1._idadb.drop_view(viewname)
    
    
@idadf_state
@timed
def su(idadf, target = None, features = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    entropy_dict = dict()
    length = len(idadf)
    corrector = np.log(length)*length
    
    if target is not None:
        value_dict = OrderedDict()
        
        entropy_dict[target] = entropy(idadf, target, mode = "raw")
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy(idadf, feature, mode = "raw")
            join_entropy = entropy(idadf, [target] + [feature], mode = "raw")
            disjoin_entropy = entropy_dict[feature] + entropy_dict[target]
            print("disjoin : %s, join: %s, entropy1 : %s, entropy2: %s"%(disjoin_entropy, join_entropy, entropy_dict[feature], entropy_dict[target]))
            value_dict[feature] = 2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(value_dict)
            result.sort(ascending = False) 
        else:
            result = value_dict[features[0]]
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
            values.append(2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2))
            
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        
    return result
    
@idadf_state
@timed
def su_noraw(idadf, target = None, features = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    entropy_dict = dict()
    
    if target is not None:
        value_dict = OrderedDict()
        
        entropy_dict[target] = entropy(idadf, target)
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy(idadf, feature)
            join_entropy = entropy(idadf, [target] + [feature])
            disjoin_entropy = entropy_dict[feature] + entropy_dict[target]
            value_dict[feature] = 2.0*(disjoin_entropy - join_entropy)/(disjoin_entropy)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(value_dict)
            result.sort(ascending = False) 
        else:
            result = value_dict[features[0]]
    else:
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]     
        
        ### Compute
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] = entropy(idadf, column_pair[0])
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] = entropy(idadf, column_pair[1])
            join_entropy = entropy(idadf,  [column_pair[0]] + [column_pair[1]])     
            disjoin_entropy = entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]]
            values.append(2.0*(disjoin_entropy - join_entropy)/(disjoin_entropy))
            
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        
    return result
    
    
@idadf_state
@timed
def su_having(idadf, target = None, features = None, having = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    target, features = _check_input(idadf, target, features)
    entropy_dict = dict()
    length = len(idadf)
    corrector = np.log(length)*length
    
    if target is not None:
        value_dict = OrderedDict()
        
        entropy_dict[target] = entropy(idadf, target, mode = "raw", having = having)
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy(idadf, feature, mode = "raw", having = having)
            join_entropy = entropy(idadf, [target] + [feature], mode = "raw", having = having)
            disjoin_entropy = entropy_dict[feature] + entropy_dict[target]
            value_dict[feature] = 2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(value_dict)
            result.sort(ascending = False) 
        else:
            result = value_dict[features[0]]
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
            values.append(2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2))
            
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        
    return result
    
@idadf_state
@timed
def su_mean(idadf, target = None, features = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    from ibmdbpy.feature_selection.entropy import entropy_mean
    # Check input
    target, features = _check_input(idadf, target, features)
    entropy_dict = dict()
    length = len(idadf)
    corrector = np.log(length)
    
    if target is not None:
        value_dict = OrderedDict()
        
        entropy_dict[target] = entropy_mean(idadf, target, mode = "raw")
        for feature in features:
            if feature not in entropy_dict:
                entropy_dict[feature] = entropy_mean(idadf, feature, mode = "raw")
            join_entropy = entropy_mean(idadf, [target] + [feature], mode = "raw")
            
            disjoin_entropy = entropy_dict[feature] + entropy_dict[target]
            print("disjoin : %s, join: %s, entropy1 : %s, entropy2: %s"%(disjoin_entropy, join_entropy, entropy_dict[feature], entropy_dict[target]))
            value_dict[feature] = 2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2)
                    
        # Output
        if len(features) > 1:
            result = pd.Series(value_dict)
            result.sort(ascending = False) 
        else:
            result = value_dict[features[0]]
    else:
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]     
        
        ### Compute
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] = entropy_mean(idadf, column_pair[0], mode = "raw")
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] = entropy_mean(idadf, column_pair[1], mode = "raw")
            join_entropy = entropy_mean(idadf,  [column_pair[0]] + [column_pair[1]], mode = "raw")     
            disjoin_entropy = entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]]
            values.append(2.0*(disjoin_entropy - join_entropy + corrector)/(disjoin_entropy + corrector*2))
            
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        
    return result
        
@idadf_state
@timed
def su_3(idadf, target , features = None, having = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, target, features)

    # Fetch data
    data = idadf.count_groupby([target], having = having) 
    
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features:
        data = idadf.count_groupby([feature] + [target], having = having) 
        feature_entropy = _compute_entropy(data, target=feature)
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)
        gain = (data_entropy - subset_entropy)
        if gain == 0: 
             value_dict[feature] = 0
        else:
            value_dict[feature] = 2.0 * (gain/(data_entropy + feature_entropy))
                
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        result.sort(ascending = False) 
        return result 
    else:
        return value_dict[features[0]]
        
@idadf_state
@timed
def su_2(idadf, target = None, features = None, having = None, version = 1):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """        
    target, features = _check_input(idadf, target, features)

    if target is None:
        ### Get data
        data = idadf.count_groupby(features, having = having)    
        
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]
        
        entropy_dict = dict()
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] =  _compute_entropy(data, target=column_pair[1])
            subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1]) 
            gain = (entropy_dict[column_pair[0]] - subset_entropy)
            if gain == 0:
                values.append(0)
            else:
                values.append(2.0 * (gain/(entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]])))
        
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        return result
    
    # Fetch data
    data = idadf.count_groupby(features + [target], having = having) 
    
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features:
        feature_entropy = _compute_entropy(data, target=feature)
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)
        gain = (data_entropy - subset_entropy)
        if gain == 0: 
             value_dict[feature] = 0
        else:
            value_dict[feature] = 2.0 * (gain/(data_entropy + feature_entropy))
               
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        result.sort(ascending = False) 
        return result 
    else:
        return value_dict[features[0]]

@idadf_state
@timed
def su_2_pareto(idadf, target = None, features = None, filter_out = 0.8, version = 1):
    # Check input
    target, features = _check_input(idadf, target, features)

    if target is None:
        if version == 1:
            count_serie = idadf.count_groupby(features, count_only = True)  # ?? + target ? 
            min_count = np.floor(count_serie.quantile(filter_out))
        if version == 2:
            min_count = idadf.min_freq_of_instance(features)
        #n_records_out = count_serie[count_serie < min_count].sum() 
        ### Get data
        data = idadf.count_groupby(features, having = min_count)    
        
        values = []
        combinations = [x for x in itertools.combinations(features, 2)]
        columns_set = [{x[0], x[1]} for x in combinations]
        
        entropy_dict = dict()
        for column_pair in combinations:
            if column_pair[0] not in entropy_dict:
                entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
            if column_pair[1] not in entropy_dict:
                entropy_dict[column_pair[1]] =  _compute_entropy(data, target=column_pair[1])
            subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1]) 
            gain = (entropy_dict[column_pair[0]] - subset_entropy)
            values.append(2.0 * (gain/(entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]])))
        
        ### Fill the matrix
        result = _fill_matrix(features, columns_set, values, 1.0)
        return result
    else:
        ### determine how much data we want
        if version == 1:
            count_serie = idadf.count_groupby(features + [target], count_only = True)  # ?? + target ? 
            min_count = np.floor(count_serie.quantile(filter_out))
        if version == 2:
            min_count = idadf.min_freq_of_instance(features + [target])
        #n_records_out = count_serie[count_serie < min_count].sum() 
            
        ### Get data
        data = idadf.count_groupby(features + [target], having = min_count)    
        
        #return data
        
        # Compute
        value_dict = OrderedDict()
        #data_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=target)
        data_entropy = _compute_entropy(data, target=target)
        
        for feature in features:
            #feature_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=feature)
            feature_entropy = _compute_entropy(data, target=feature)
            #subset_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=target, conditional=feature)
            subset_entropy = _compute_entropy(data, target=target, conditional=feature)
            gain = (data_entropy - subset_entropy)
            symmetrical_uncertainty = 2.0 * (gain/(data_entropy + feature_entropy))
    
            value_dict[feature] = symmetrical_uncertainty   
       
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        result.sort(ascending = False) 
        return result 
    else:
        return value_dict[features[0]]   
       
@idadf_state
@timed
def su_1(idadf, target , features = None):
    target, features = _check_input(idadf, target, features)

    value_dict = OrderedDict()
    
    data_entropy = entropy(idadf, target)
    
    for feature in features:
        feature_entropy = entropy(idadf, feature)
        subset_entropy = 0.0
        attr_values = idadf.unique(feature)
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            subset_entropy += factor*entropy(subset, target)   #### += ???

        gain = (data_entropy - subset_entropy)
        symmetrical_uncertainty = 2.0 * (gain/(data_entropy + feature_entropy))

        value_dict[feature] = symmetrical_uncertainty   
        
    if len(features) > 1:
        result = pd.Series(value_dict)
        result.sort(ascending = False) 
        return result 
    else:
        return value_dict[features[0]]   