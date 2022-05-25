# -*- coding: utf-8 -*-
""" This module contains the functions to help in analysis of data"""
import sys
import pandas as pd


def _type_list(series):
    """
    This shadow function return the unique type not None list.
    
    For identify the no-None objet, it uses the ``pandas.notnull`` function
    :param series: Series objets who contains data to analysis 
    :type series: iterative object
    :return: unique no-None type list
    :rtype: list
    """
    if not isinstance(series, pd.Series):
        raise TypeError(f"_type_list : le type attendu est pandas.Series. Le type est {type(series)}")
    _result = series[series.notnull()].map(lambda x: type(x).__name__).unique()
    if len(_result)==0:
        return 'None'
    elif len(_result)==1:
        return _result[0]
    else:
        return '>, <'.join(_result)

def summarize(dataset=None, size_head=50, output = sys.stdout):
    """
    This function returns a summary of information about the DataFrame.
    The informations is printing to standard output and are :
        - The column name
        - The type of data (issue of the dtype property)
        - The count of not null- data and its percentage
        - The head of unique values
    """
    if isinstance(dataset, pd.DataFrame):
        datatype = dataset.dtypes
        print(f"Shape : {dataset.shape}", file=output)
        for col in dataset.columns:
            col_notnull_size = len(dataset[~dataset[col].isnull()][col])
            print("{col_name:<10} : {col_type:<10} : {col_size} : [{col_value}]"
                  .format(col_name=col,
                          col_type=f"<{_type_list(dataset.loc[:,col])}>",
                          col_size=f"{col_notnull_size} ({col_notnull_size/len(dataset[col])*100:0.2f} %)",
                          col_value=f"{str(dataset[dataset[col].notnull()][col].unique())[1:-1][:size_head]}")
                  , file=output
                  )
