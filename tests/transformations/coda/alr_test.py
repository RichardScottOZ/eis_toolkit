import numpy as np
import pandas as pd
import pytest

from eis_toolkit.exceptions import InvalidColumnException, InvalidColumnIndexException, InvalidParameterValueException
from eis_toolkit.transformations.coda.alr import _ALR_transform

ONES_DATAFRAME_4x4 = pd.DataFrame(np.ones((4, 4)), columns=["c1", "c2", "c3", "c4"])

ZEROS_DATAFRAME_4x3 = pd.DataFrame(np.zeros((4, 3)), columns=["c1", "c2", "c3"])

SAMPLE_DATAFRAME = pd.DataFrame(
    np.array(
        [
            [0.000584, 0.000430, 0.000861, 0.000129],
            [0.000170, 0.000537, 0.000441, 0.000012],
            [0.000286, 0.000365, 0.000131, 0.000009],
            [0.000442, 0.000199, 0.000075, 0.000063],
            [0.000366, 0.000208, 0.000116, 0.000255],
            [0.000310, 0.000041, 0.000219, 0.000086],
            [0.000229, 0.000354, 0.000441, 0.000529],
            [0.000245, 0.000088, 0.000310, 0.000220],
            [0.000317, 0.000446, 0.000946, 0.000090],
            [0.000198, 0.000160, 0.000474, 0.000068],
        ]
    ),
    columns=["c1", "c2", "c3", "c4"],
)


def test_alr_transform_simple():
    """TODO: docstring."""
    output = _ALR_transform(ONES_DATAFRAME_4x4)
    pd.testing.assert_frame_equal(output, ZEROS_DATAFRAME_4x3)


def test_alr_transform():
    """TODO: docstring."""
    return


def test_alr_transform_contains_zeros():
    """TODO: docstring."""
    with pytest.raises(InvalidColumnException):
        zeros_data = SAMPLE_DATAFRAME.copy()
        zeros_data.iloc[0, 0] = 0
        _ALR_transform(zeros_data)


def test_alr_transform_with_unexpected_column_name():
    """TODO: docstring."""
    with pytest.raises(InvalidColumnException):
        _ALR_transform(SAMPLE_DATAFRAME, ["c1", "c2", "comp3"])


def test_alr_transform_with_out_of_bounds_denominator_column():
    """TODO: docstring."""
    with pytest.raises(InvalidColumnIndexException):
        _ALR_transform(SAMPLE_DATAFRAME, None, -5)


def test_alr_transform_with_too_few_columns():
    """TODO: docstring."""
    with pytest.raises(InvalidParameterValueException):
        _ALR_transform(SAMPLE_DATAFRAME, ["c1"])


def test_alr_transform_with_nonnumeric_index():
    """TODO: docstring."""
    return


def test_alr_transform_redundant_column():
    """TODO: docstring."""
    return


# TODO: test with unnamed columns