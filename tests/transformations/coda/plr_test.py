import numpy as np
import pandas as pd
import pytest

from eis_toolkit.exceptions import InvalidColumnException
from eis_toolkit.transformations.coda.plr import PLR_transform, _single_PLR_transform_index, single_PLR_transform


def test_single_PLR_transform_with_single_composition():
    """Test a single PLR transform operation with a single composition."""
    c_arr = np.array([80, 15, 5])
    C = pd.DataFrame(c_arr[None], columns=["a", "b", "c"])

    result = single_PLR_transform(C, "a")
    assert result[0] == pytest.approx(1.82, abs=1e-2)

    result = _single_PLR_transform_index(C, 0)
    assert result[0] == pytest.approx(1.82, abs=1e-2)

    result = single_PLR_transform(C, "b")
    assert result[0] == pytest.approx(0.78, abs=1e-2)

    result = _single_PLR_transform_index(C, 1)
    assert result[0] == pytest.approx(0.78, abs=1e-2)


def test_single_PLR_transform_with_simple_data():
    """Test single PLR transform core functionality."""
    c_arr = np.array([[80, 15, 5], [75, 18, 7]])
    C = pd.DataFrame(c_arr, columns=["a", "b", "c"])
    result = single_PLR_transform(C, "b")
    assert result[1] == pytest.approx(0.67, abs=1e-2)


def test_single_PLR_transform_with_last_column():
    """Test that selecting the last part of the composition as the input column raises the correct exception."""
    with pytest.raises(InvalidColumnException):
        c_arr = np.array([[80, 15, 5], [75, 18, 7]])
        C = pd.DataFrame(c_arr, columns=["a", "b", "c"])
        single_PLR_transform(C, "c")


def test_PLR_transform():
    """Test PLR transform core functionality."""
    c_arr = np.array([[65, 12, 18, 5], [63, 16, 15, 6]])
    C = pd.DataFrame(c_arr, columns=["a", "b", "c", "d"])
    result = PLR_transform(C)
    assert len(result.columns) == len(C.columns) - 1
    expected = pd.DataFrame(np.array([[1.60, 0.19, 0.91], [1.49, 0.43, 0.65]]), columns=["a", "b", "c"])
    pd.testing.assert_frame_equal(result, expected, atol=1e-2)


def test_PLR_transform_with_zeros():
    """Test that running the transformation for a dataframe containing zeros raises the correct exception."""
    with pytest.raises(InvalidColumnException):
        df = pd.DataFrame(np.zeros((3, 3)), columns=["a", "b", "c"])
        PLR_transform(df)