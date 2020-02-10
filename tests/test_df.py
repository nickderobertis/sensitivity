import pandas as pd
from pandas.testing import assert_frame_equal

from sensitivity.df import sensitivity_df
from tests.base import EXPECT_DF, SENSITIVITY_VALUES, add_5_to_values, RESULT_NAME


def test_create_sensitivity_df():
    df = sensitivity_df(
        SENSITIVITY_VALUES,
        add_5_to_values,
        result_name=RESULT_NAME
    )

    assert_frame_equal(df, EXPECT_DF, check_dtype=False)
