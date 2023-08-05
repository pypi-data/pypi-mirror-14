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

from ibmdbpy.feature_selection.measures import pearson
from ibmdbpy.feature_selection.info_gain import info_gain
from ibmdbpy.feature_selection.gain_ratio import gain_ratio
import pandas as pd

import six

class SelectKBest(object):
    
    def __init__(self, score_func, k=10):
        if score_func not in ['corr']:
            raise ValueError("Unknown score function %s"%score_func)
        if not (isinstance(k, six.integer_types)|(k == "all")):
            raise ValueError("Admissible values for k are postive integer or \"all\" ")      
        if isinstance(k, six.integer_types):
            if not k > 0:
                raise ValueError("k should be stricly positive")
        
        self._score_func = score_func
        self._k = k
        
    def fit(self, idadf, target):
        if target not in idadf:
            raise ValueError("Target attribute %s does not exist in the given IdaDataFrame"%target)
        
        if self._score_func == "pearson":    
            self.scores_ = pearson(idadf, target)
        if self._score_func == "info_gain":
            self.scores_ = info_gain(idadf, target)
        if self._score_func == "info_gain_ratio":
            self.scores_ = gain_ratio(idadf, target)
        
    def fit_transform(self, idadf, target):
        self.fit(idadf, target)
        abs_scores = self.scores_.abs()
        sorted_abs_scores = abs_scores.sort(ascending=False, inplace = False)
        features = list(sorted_abs_scores[0:self._k].index)
        return idadf[features]
        
        