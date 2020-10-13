import pandas as pd
from pandas.testing import assert_frame_equal

from sensitivity.df import sensitivity_df
from tests.base import EXPECT_DF_TWO_VALUE, SENSITIVITY_VALUES_TWO_VALUE, add_5_to_values, RESULT_NAME, \
    TWO_VALUE_LABELS, EXPECT_DF_TWO_VALUE_LABELS


def test_create_sensitivity_df():
    df = sensitivity_df(
        SENSITIVITY_VALUES_TWO_VALUE,
        add_5_to_values,
        result_name=RESULT_NAME
    )

    assert_frame_equal(df, EXPECT_DF_TWO_VALUE, check_dtype=False)


def test_labeled_sensitivity_df():
    df = sensitivity_df(
        SENSITIVITY_VALUES_TWO_VALUE,
        add_5_to_values,
        result_name=RESULT_NAME,
        labels=TWO_VALUE_LABELS
    )

    assert_frame_equal(df, EXPECT_DF_TWO_VALUE_LABELS, check_dtype=False)