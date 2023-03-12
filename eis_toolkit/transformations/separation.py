
from typing import Tuple
import pandas as pd
from eis_toolkit.exceptions import InvalidParameterValueException, InvalideContentOfInputDataFrame
# *******************************
def _separation(
    df: pd.DataFrame,
    fields: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:            # Xvdf, Xcdf, ydf, ,

    cn = df.columns
    ### Target dataframe
    name = {i for i in fields if fields[i]=='t'}
    if not set(list(name)).issubset(set(cn)):
        raise InvalideContentOfInputDataFrame('fields and column names of DataFrame df does not match')
    ydf = df[list(name)]       #ydf = Xdf.loc[:,name]
    #Xdf.drop(name, axis=1, inplace=True)

    ### Values dataframe
    name ={i for i in fields if fields[i] in ('v','b')}
    if not set(list(name)).issubset(set(cn)):
        raise InvalideContentOfInputDataFrame('fields and column names of DataFrame df does not match')
    Xvdf = df[list(name)]       #ydf = Xdf.loc[:,name]
    #Xdf.drop(name, axis=1, inplace=True)

    ### classes dataframe
    name = {i for i in fields if fields[i] == 'c'}
    if not set(list(name)).issubset(set(cn)):
        raise InvalideContentOfInputDataFrame('fields and column names of DataFrame df does not match')
    Xcdf = df[list(name)]       #ydf = Xdf.loc[:,name]
    #Xdf.drop(name, axis=1, inplace=True)    

    ### identity-geometry dataframe
    name = {i for i in fields if fields[i] in ('i','g')}
    if not set(list(name)).issubset(set(cn)):
        raise InvalideContentOfInputDataFrame('fields and column names of DataFrame df does not match')
    igdf = df[list(name)]       #ydf = Xdf.loc[:,name]
    #Xdf.drop(name, axis=1, inplace=True)   


    return Xvdf, Xcdf, ydf, igdf

# *******************************
def separation(  # type: ignore[no-any-unimported]
    df: pd.DataFrame,
    fields: dict
) -> Tuple[pd.DataFrame,pd.DataFrame, pd.DataFrame,pd.DataFrame]:

    """
        Separates the target column (id exists) to a separate dataframe ydf
        All categorical columns (fields) will be separated from all other features (columns) in a separate dataframe Xcdf.
        Separates the id and geometry column to a separate dataframe igdf
    Args:
        df (pandas DataFrame): Including target column ('t').
        fields (dictionary): Column type for each column

    Returns:
        pandas DataFrame: value-sample  (Xvdf)
        pandas DataFrame: categorical columns (Xcdf)
        pandas DataFrame: target (ydf)
        pandas DataFrame: target (igdf)
    """

    # Argument evaluation
    fl = []
    if not (isinstance(df, pd.DataFrame)):
        fl.append('Argument df is not a DataFrame')
    if not (isinstance(fields, dict)):
        fl.append('Argument fields is not a dictionary') 
    if len(fl) > 0:
        raise InvalidParameterValueException (fl[0])
        
    if len(df.columns) == 0:
        raise InvalideContentOfInputDataFrame('DataFrame has no column')
    if len(df.index) == 0:
        raise InvalideContentOfInputDataFrame('DataFrame has no rows')
    if len(fields) == 0:
        raise InvalideContentOfInputDataFrame('Fields is empty')

    # call
    return _separation(df, fields)

