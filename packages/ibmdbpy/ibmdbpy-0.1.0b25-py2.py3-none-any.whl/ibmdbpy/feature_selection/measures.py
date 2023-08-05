#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2015, IBM Corp.
# All rights reserved.
#
# Distributed under the terms of the BSD Simplified License.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------

#from numbers import Number
from collections import OrderedDict

#from ibmdbpy.feature_selection import entropy

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

import numpy as np
#from numpy import log2
import pandas as pd

import six

#import ibmdbpy

@idadf_state
@timed
def pearson(idadf, target, feature_list = None):
    numerical_columns = idadf._get_numerical_columns()
    if target not in numerical_columns:
        raise TypeError("Correlation-based measure not available for non-numerical target %s"%target)
    
    if feature_list is None:
        feature_list = [x for x in idadf.columns if x != target]
    else:
        if isinstance(feature_list, six.string_types):
            feature_list = [feature_list]
        # make sure the target is not in feature_list
        if target in feature_list:
            feature_list = [x for x in feature_list if x != target]
    
    numerical_features = [x for x in feature_list if x in numerical_columns]
    agg_list = ["CORRELATION(\"%s\",\"%s\")"%(x, target) for x in numerical_features]
    agg_string = ', '.join(agg_list)
    
    name = idadf.internal_state.current_state
    data = idadf.ida_query("SELECT %s FROM %s"%(agg_string, name), first_row_only = True)
    
    if len(feature_list) > 1:
        value_dict = OrderedDict()
        i = 0
        for feature in feature_list:
            if feature not in numerical_columns:
                value_dict[feature] = np.nan
            else:
                value_dict[feature] = data[i]
                i += 1  
        result = pd.Series(value_dict)
        result.index = feature_list
        return result 
    else:
        if feature_list[0] not in numerical_columns:
            return np.nan
        else:
            return data[0]
 
        
        

        