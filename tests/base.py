from copy import deepcopy

import pandas as pd

RESULT_NAME = 'my_res'
EXPECT_DF_TWO_VALUE = pd.DataFrame(
    [
        (1, 4, 10),
        (1, 5, 11),
        (2, 4, 11),
        (2, 5, 12),
    ],
    columns=['value1', 'value2', RESULT_NAME]
)

EXPECT_DF_THREE_VALUE = pd.DataFrame(
    [
        (1, 4, 6, 21),
        (1, 4, 7, 22),
        (1, 5, 6, 22),
        (1, 5, 7, 23),
        (2, 4, 6, 22),
        (2, 4, 7, 23),
        (2, 5, 6, 23),
        (2, 5, 7, 24),
    ],
    columns=['value1', 'value2', 'value3', RESULT_NAME]
)

SENSITIVITY_VALUES_TWO_VALUE = {
    'value1': [1, 2],
    'value2': [4, 5],
}
SENSITIVITY_VALUES_THREE_VALUE = deepcopy(SENSITIVITY_VALUES_TWO_VALUE)
SENSITIVITY_VALUES_THREE_VALUE['value3'] = [6, 7]


def add_5_to_values(value1, value2):
    return value1 + value2 + 5

def add_10_to_values(value1, value2, value3=5):
    return value1 + value2 + value3 + 10

