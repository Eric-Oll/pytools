# -*- coding: utf-8 -*-
""" This module contains the functions to help in analysis of data"""

import pandas as pd


def summarize(dataset=None, size_head=50):
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
        print(f"Shape : {dataset.shape}")
        for col in dataset.columns:
            col_notnull_size = len(dataset[~dataset[col].isnull()][col])
            print("{col_name:<10} : {col_type:<10} : {col_size} : [{col_value}]"
                  .format(col_name=col,
                          col_type=f"<{datatype[col].name}>",
                          col_size=f"{col_notnull_size} ({col_notnull_size/len(dataset[col])*100:0.2f} %)",
                          col_value=f"{str(dataset[col].unique())[1:-1][:size_head]}"))
