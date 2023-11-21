import numpy as np
import pandas as pd
from beartype import beartype
from scipy.stats import gmean

from eis_toolkit.exceptions import InvalidColumnException, InvalidParameterValueException
from eis_toolkit.utilities.checks.dataframe import check_dataframe_contains_zeros
from eis_toolkit.utilities.checks.parameter import check_numeric_value_sign


@beartype
def _calculate_scaling_factor(c: int) -> np.float64:
    """
    Calculate the scaling factor for the PLR transform.

    Args:
        c: The cardinality of the remaining parts in the composition.

    Returns:
        The scaling factor used performing a single PLR transform for a composition.

    Raises:
        InvalidParameterValueException: The input value is zero or negative.
    """
    if not (check_numeric_value_sign(c)):
        raise InvalidParameterValueException("The input value must be a positive integer.")

    return np.sqrt(c / np.float64(1 + c))


@beartype
def _single_PLR_transform_index(df: pd.DataFrame, column_ind: int) -> pd.Series:
    dfc = df.copy()
    # The denominator is a subcomposition of all the parts "to the right" of the column:
    columns = [col for col in df.columns]
    subcomposition = [columns[i] for i in range(len(columns)) if i > column_ind]
    c = len(subcomposition)
    scaling_factor = _calculate_scaling_factor(c)

    # A series to hold the transformed rows
    plr_values = pd.Series([0.0] * df.shape[0])

    for idx, row in dfc.iterrows():
        plr_values[idx] = scaling_factor * np.log(row.iloc[column_ind] / gmean(row[subcomposition]))

    return plr_values


@beartype
def _single_PLR_transform(df: pd.DataFrame, column: str) -> pd.Series:
    dfc = df.copy()
    idx = dfc.columns.get_loc(column)

    # The denominator is a subcomposition of all the parts "to the right" of the column:
    columns = [col for col in df.columns]
    subcomposition = [columns[i] for i in range(len(columns)) if i > idx]
    c = len(subcomposition)
    scaling_factor = _calculate_scaling_factor(c)

    # A series to hold the transformed rows
    plr_values = pd.Series([0.0] * df.shape[0])

    for idx, row in dfc.iterrows():
        plr_values[idx] = scaling_factor * np.log(row[column] / gmean(row[subcomposition]))

    plr_values = plr_values.T
    return plr_values


@beartype
def single_PLR_transform(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Perform a pivot logratio transformation on the selected column.

    Pivot logratio is a special case of ILR, where the numerator in the ratio is always a single
    part and the denominator all of the parts to the right in the ordered list of parts.

    Column order matters.

    Args:
        df: A dataframe of shape [N, D] of compositional data.
        column: The name of the numerator column to use for the transformation.

    Returns:
        A series of length N containing the transforms.

    Raises:
        InvalidColumnException: The input column isn't found in the dataframe, or there are no columns
            to the right of the given column.
    """

    if column not in df.columns:
        raise InvalidColumnException()

    idx = df.columns.get_loc(column)

    if idx == len(df.columns) - 1:
        raise InvalidColumnException()

    return _single_PLR_transform(df, column)


@beartype
def _PLR_transform(df: pd.DataFrame) -> pd.DataFrame:
    dfc = df.copy()

    # A dataframe to hold the transformed values
    plr_values = pd.DataFrame(0.0, index=dfc.index, columns=dfc.columns[:-1])

    for i in range(len(df.columns) - 1):
        plr_values.iloc[:, i] = _single_PLR_transform_index(dfc, i)

    return plr_values


@beartype
def PLR_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform a pivot logratio transformation on the dataframe, returning the full set of transforms.

    Args:
        df: A dataframe of shape [N, D] of compositional data.

    Returns:
        A dataframe of shape [N, D-1] containing the set of PLR transformed data.

    Raises:
        InvalidColumnException: The data contains one or more zeros.
    """
    # TODO: possibly allow performing PLR transform for a subcomposition
    if check_dataframe_contains_zeros(df):
        raise InvalidColumnException("The dataframe contains one or more zeros.")

    return _PLR_transform(df)


@beartype
def _inverse_PLR():
    raise NotImplementedError()