# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:49:45 2015

@author: efouche
"""

from numpy import log2

###############################################################################
##### Memory equivalent 
###############################################################################
    
def entropy_mem(data, target_attr):
 
    val_freq = {}
    data_entropy = 0.0
 
    # Calculate the frequency of each of the values in the target attr
    val_freq = data[target_attr].value_counts()
     
    # Calculate the entropy of the data for the target attribute
    for freq in val_freq:
        info = freq/len(data)
        data_entropy += ((-info) * log2(info))
 
    return data_entropy
    
def info_gain_mem(data, target_attr, attr):
    
    val_freq = {}
    subset_entropy = 0.0
 
    # Calculate the frequency of each of the values in the attr
    val_freq = data[attr].value_counts()
    
    # Calculate the sum of the entropy for each subset of records weighted by their probability of occuring in the training set.
    for val in val_freq.index:
        val_prob = val_freq[val] / val_freq.sum()
        data_subset = data[data[attr] == val]
        subset_entropy += val_prob * entropy_mem(data_subset, target_attr)
 
    # Subtract the entropy of the chosen attribute from the entropy of the whole data set with respect to the target attribute (and return it)
    return (entropy_mem(data, target_attr) - subset_entropy)