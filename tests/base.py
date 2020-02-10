import pandas as pd

RESULT_NAME = 'my_res'
EXPECT_DF = pd.DataFrame(
    [
        (1, 4, 10),
        (1, 5, 11),
        (2, 4, 11),
        (2, 5, 12),
    ],
    columns=['value1', 'value2', RESULT_NAME]
)

SENSITIVITY_VALUES = {
    'value1': [1, 2],
    'value2': [4, 5],
}


def add_5_to_values(value1, value2):
    return value1 + value2 + 5
