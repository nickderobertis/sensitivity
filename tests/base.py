import os
from copy import deepcopy
from io import BytesIO
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from pandas.io.formats.style import Styler
import matplotlib.pyplot as plt

INPUT_FILES_FOLDER = Path(__file__).parent / "input_data"
DF_STYLED_PATH = os.path.join(INPUT_FILES_FOLDER, 'df_styled.html')
DF_LABELED_PATH = os.path.join(INPUT_FILES_FOLDER, 'df_labeled.html')
DF_STYLED_NUM_FMT_PATH = os.path.join(INPUT_FILES_FOLDER, 'df_styled_num_fmt.html')
DF_STYLE_UUID = '1ee5ad65-4cac-42e3-8133-7ae800cb23ad'
DEFAULT_PLOT_PATH = INPUT_FILES_FOLDER / 'default_plot.png'
PLOT_THREE_PATH = INPUT_FILES_FOLDER / 'plot_three.png'
PLOT_OPTIONS_PATH = INPUT_FILES_FOLDER / 'plot_options.png'
RESULT_NAME = 'my_res'
TWO_VALUE_LABELS = {
    'value1': 'Formatted 1',
    'value2': 'Formatted 2'
}
THREE_VALUE_LABELS = deepcopy(TWO_VALUE_LABELS)
THREE_VALUE_LABELS['value3'] = 'Formatted 3'
EXPECT_DF_TWO_VALUE = pd.DataFrame(
    [
        (1, 4, 10),
        (1, 5, 11),
        (2, 4, 11),
        (2, 5, 12),
    ],
    columns=['value1', 'value2', RESULT_NAME]
)
EXPECT_DF_TWO_VALUE_LABELS = EXPECT_DF_TWO_VALUE.rename(columns=TWO_VALUE_LABELS)

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


def assert_styled_matches(styler: Styler, file_path: str = DF_STYLED_PATH, generate: bool = False):
    compare_html = styler.set_uuid(DF_STYLE_UUID).to_html()

    if generate:
        Path(file_path).write_text(_prettify_html(compare_html))

    with open(file_path, 'r') as f:
        expect_html = f.read()

    assert _prettify_html(compare_html) == _prettify_html(expect_html)


def _prettify_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()


def assert_graph_matches(fig: plt.Figure, file_path: Path = DEFAULT_PLOT_PATH, generate: bool = False):
    if generate:
        fig.savefig(str(file_path))

    compare_bytestream = BytesIO()
    fig.savefig(compare_bytestream)
    compare_bytestream.seek(0)
    compare_bytes = compare_bytestream.read()

    expect_bytes = file_path.read_bytes()

    assert compare_bytes == expect_bytes




