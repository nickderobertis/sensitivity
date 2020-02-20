import os
from copy import deepcopy

import pandas as pd
from pandas.io.formats.style import Styler

INPUT_FILES_FOLDER = os.path.join('tests', 'input_data')
DF_STYLED_PATH = os.path.join(INPUT_FILES_FOLDER, 'df_styled.html')
DF_STYLED_NUM_FMT_PATH = os.path.join(INPUT_FILES_FOLDER, 'df_styled_num_fmt.html')
DF_STYLE_UUID = '1ee5ad65-4cac-42e3-8133-7ae800cb23ad'
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


def assert_styled_matches(styler: Styler, file_path: str = DF_STYLED_PATH):
    with open(file_path, 'r') as f:
        expect_html = f.read()

    compare_html = styler.set_uuid(DF_STYLE_UUID).render()
    assert compare_html == expect_html
