import pandas as pd
from pandas.testing import assert_frame_equal

from sensitivity.df import sensitivity_df


def add_5_to_values(value1, value2):
    return value1 + value2 + 5


def test_create_sensitivity_df():
    expect_df = pd.DataFrame(
        [
            (1, 4, 10),
            (1, 5, 11),
            (2, 4, 11),
            (2, 5, 12),
        ],
        columns=['value1', 'value2', 'my_res']
    )

    df = sensitivity_df(
        {
            'value1': [1, 2,],
            'value2': [4, 5,],
        },
        add_5_to_values,
        result_name='my_res'
    )

    assert_frame_equal(df, expect_df, check_dtype=False)
