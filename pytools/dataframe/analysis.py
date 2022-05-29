# -*- coding: utf-8 -*-
""" This module contains the functions to help in analysis of data"""
import pstats
import sys
import pandas as pd
from IPython.display import HTML

DEFAULT_OUTPUT = sys.stdout

# Constant of result dict
SHAPE = "SHAPE"
DESCRIPTION = "DESCRIPTION"
INDEX = 'INDEX'

HTML_MODEL = """
<div>
    <p style="text-decoration:underline">Taille des données</p>
    <ul>
        <li>Nombre de lignes : <strong>{nb_lig}</strong></li>
        <li>Nombre de colonnes : {nb_col}</li>
    </ul>
    <p style="text-decoration:underline">Description</p>
    {description}
</div>
"""


def _html_formatter(analysis_dict, html_model=HTML_MODEL):
    """
    Formatter function 
    :param analysis_dict: Analysis result with 
            {
            SHAPE: size of frame, 
            DESCRIPTION: data's description,
            } 
    :type analysis_dict: dict
    :param html_model: Model for HTML
    :type html_model: str
    :return: HTML format
    :rtype: str
    """
    return html_model.format(
        nb_lig=analysis_dict[SHAPE][0],
        nb_col=analysis_dict[SHAPE][1],
        description=analysis_dict[DESCRIPTION].style.hide(axis='index').format({
            'TYPE': lambda l: ', '.join(l) if isinstance(l, list) else l,
            'FILLING': "{:.2%}"
        }).to_html()
    )


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
    if len(_result) == 0:
        return '<None>'
    elif len(_result) == 1:
        return _result[0]
    else:
        return list(_result)


def _min_value(series, type_list=None):
    """
    Défine the min value of the series :
    - for 'str' type it's the min lenght of the string value
    - for 'int' or 'float' type, it's the min value of the serie
    for other type, this function return 'None'
    :param series: 
    :type series: 
    :param type_list: 
    :type type_list: 
    :return: 
    :rtype: 
    """
    if type_list is None:
        type_list = _type_list(series)

    if isinstance(type_list, str) and type_list == 'str':
        return min(series[series.notnull()].map(len))
    elif isinstance(type_list, str) and (type_list == 'int' or type_list == 'float'):
        return series[series.notnull()].min()
    else:
        return None


def _max_value(series, type_list=None):
    """
    Défine the max value of the series :
    - for 'str' type it's the max lenght of the string value
    - for 'int' or 'float' type, it's the max value of the serie
    for other type, this function return 'None'
    :param series: 
    :type series: 
    :param type_list: 
    :type type_list: 
    :return: 
    :rtype: 
    """
    if type_list is None:
        type_list = _type_list(series)

    if isinstance(type_list, str) and type_list == 'str':
        return max(series[series.notnull()].map(len))
    elif isinstance(type_list, str) and (type_list == 'int' or type_list == 'float'):
        return series[series.notnull()].max()
    else:
        return None


def summarize(dataset=None, size_head=80, output=DEFAULT_OUTPUT, html_formatter=_html_formatter):
    """
    This function returns a summary of information about the DataFrame.
    The informations is printing to standard output and are :
        - The column name
        - The type of data
        - The count of not null- data and its percentage
        - The head of unique values
    :param dataset: Object to analysis
    :type dataset: pandas.DataFrame
    :param size_head: max lenght of header of data's example
    :type size_head: int
    :param output: 
        IO Object : writable object (ie. object with `write` function with string argument
        'HTML' : output in HTML format
        'DICT' : Analysis result : dictionnary with 
            {
            SHAPE: size of frame, 
            DESCRIPTION: data's description,
            INDEX: index's description
            } 
    :return: None if IO Object else type of selected output 
    """
    if isinstance(dataset, pd.DataFrame):
        _result = {
            SHAPE: dataset.shape,
            DESCRIPTION: pd.DataFrame(columns=['NAME', 'TYPE', 'COUNT', 'FILLING', 'MIN', 'MAX', 'SAMPLE'],
                                      index=dataset.columns),
            INDEX: pd.DataFrame(columns=['NAME', 'TYPE', 'N_UNIQUE', 'SAMPLE'], index=dataset.index.names),
        }
        # Description des données
        for col in dataset.columns:
            col_notnull_size = len(dataset[~dataset[col].isnull()][col])
            _result[DESCRIPTION].at[col, 'NAME'] = col
            _result[DESCRIPTION].at[col, 'TYPE'] = _type_list(dataset.loc[:, col])
            _result[DESCRIPTION].at[col, 'COUNT'] = col_notnull_size
            _result[DESCRIPTION].loc[col, 'FILLING'] = col_notnull_size / len(dataset) if len(dataset) > 0 else 0
            _result[DESCRIPTION].loc[col, 'MIN'] = _min_value(dataset.loc[:, col],
                                                              _result[DESCRIPTION].loc[col, 'TYPE'])
            _result[DESCRIPTION].loc[col, 'MAX'] = _max_value(dataset.loc[:, col],
                                                              _result[DESCRIPTION].loc[col, 'TYPE'])
            _result[DESCRIPTION].loc[col, 'SAMPLE'] = str(dataset[dataset[col].notnull()][col].unique())[1:-1][
                                                      :size_head]

        # Description de l'index
        for name in dataset.index.names:
            _result[INDEX].loc[name, 'NAME'] = name
            _result[INDEX].loc[name, 'TYPE'] = dataset.index.get_level_values(name).map(
                lambda x: type(x).__name__).unique()
            _result[INDEX].loc[name, 'N_UNIQUE'] = dataset.index.get_level_values(name).nunique()
            _result[INDEX].loc[name, 'N_UNIQUE'] = str(dataset.index.get_level_values(name).unique())[1:-1][:size_head]
    else:
        raise TypeError(
            f"Le type d'objet à analyser doit être au format `pandas.DataFrame`.\nLe type d'objet en entrée est de type {type(dataset)}")

    if isinstance(output, str):
        if output == 'DICT':
            return _result
        elif output == 'HTML':
            return HTML(_html_formatter(_result))
    else:
        print(f"Shape : {_result[SHAPE]}", file=output)
        for idx, row in _result[DESCRIPTION].iterrows():
            print("{col_name:<10} : {col_type:<10} {col_limite} : {col_size} : [{col_value}]"
                  .format(col_name=row.NAME,
                          col_type=', '.join(row.TYPE) if isinstance(row.TYPE, list) else row.TYPE,
                          col_limite=f"[{int(row.MIN)}, {int(row.MAX)}]" if pd.notnull(row.MIN) else '',
                          col_size=f"{row.COUNT} ({row.FILLING:0.2%})",
                          col_value=row.SAMPLE
                          )
                  , file=output
                  )
        return None