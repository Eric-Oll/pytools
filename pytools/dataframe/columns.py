"""
Module contenant les fonctions utile sur les colonnes de DataFrame

"""
import pandas as pd

def rename_duplicated_columns(df:pd.DataFrame, inplace=False)->list:
    """
    Renomme les colonnes en plusieurs exemplaires
    :param df: DataFrame
    :param inplace:
        - True: applique le renommage à l'objet 'df'
        - False (defaut): Ne change pas l'objet 'df' et ne retourne rien
    :return: Retourne la liste des colonnes dédoublonnées
    """
    column_count = dict()
    new_columns = []
    for col in df.columns:
        column_count[col] = column_count.get(col, -1) + 1
        if column_count[col] == 0:
            new_columns.append(col)
        else:
            new_columns.append(f"{col}_{column_count[col]}")

    if inplace:
        df.columns = new_columns
    else:
        return new_columns

