# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:53:55 2018

@author: Eric
"""
import pandas as pd

def read_dict(list_of_dict):
    """
    Create a DataFrame from a dict or a list of dict.
    - Each key of dict generate a columns of the DataFrame result
    - Each item of the list generate a line of the DataFrame result
      => For a dict-only, only one line is contained into the DataFrame result
    """
    
    # Transform the dict in dict's list
    if isinstance(list_of_dict,dict):
        _list_dict = []
        _list_dict.append(list_of_dict)
    elif isinstance(list_of_dict, list):
        _list_dict = list_of_dict
    else:
        raise TypeError('Type unexpected for list_of_dict.')
        return None
        
    # Add data into DataFrame
    result = pd.DataFrame()
    for item in _list_dict:
        result = result.append(item, ignore_index=True)
    
    return result
