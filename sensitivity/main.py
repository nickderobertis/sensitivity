import itertools
from dataclasses import dataclass
from typing import Dict, Any, Callable, Optional, List, Union, Sequence

import numpy as np
import pandas as pd
from pandas.io.formats.style import Styler
import matplotlib.pyplot as plt
from IPython.display import display, HTML

from sensitivity.df import sensitivity_df, _style_sensitivity_df, _two_variable_sensitivity_display_df
from sensitivity.hexbin import _hex_figure_from_sensitivity_df


@dataclass
class SensitivityAnalyzer:
    """
    Runs sensitivity analysis based on the passed function and possible values for each argument.

    Runs func with the cartesian product of the possible values for each argument, passed
    in sensitivity_values. Exposes the DataFrame containing the results, a styled version of
    the DataFrame, and a Hex-Bin plot.

    :param sensitivity_values: Dictionary where keys are func's argument names and values are lists of possible
        values to use for that argument.
    :param func: Function that accepts arguments with names matching the keys of sensitivity_values, and outputs a
        scalar value.
    :param result_name: Name for result shown in graph color bar label
    :param agg_func: If there are multiple results within the hex parameter area, function to aggregate those results to
        get a single value for the hex area. The function should accept a sequence of values and return a scalar.
    :param reverse_colors: Default is for red to represent low values of result, green for high values. Set
        reverse_colors=True to have green represent low values of result and red for high values.
    :param grid_size: Number of hex bins on each axis. E.g. passing 5 would create a 5x5 grid, 25 hex bins.
    :param func_kwargs: Additional arguments to pass to func, regardless of the sensitivity values picked
    :param num_fmt: used to apply additional styling to DataFrames. Should be a number format string in the
        same style as would be passed to df.style.format, e.g. '${:,.2f}' for USD formatting
    :param color_map: matplotlib color map, default is RdYlGn (red, yellow, green). See
        https://matplotlib.org/3.3.2/tutorials/colors/colormaps.html
    :param labels: Optional dictionary where keys are arguments of the function and values are the displayed names
        for these arguments in the styled DataFrames and plots
    :return: Sensitivity analysis hex bin sub plot figure

    Examples:
        >>> from sensitivity import SensitivityAnalyzer
        >>>
        >>> # Some example function
        >>> def add_5_to_values(value1, value2):
        >>>     return value1 + value2 + 5
        >>>
        >>> # The values to be passed for each parameter of the function
        >>> sensitivity_values = {
        >>>     'value1': [1, 2, 3],
        >>>     'value2': [4, 5, 6],
        >>> }
        >>>
        >>> sa = SensitivityAnalyzer(
        >>>     sensitivity_values,
        >>>     add_5_to_values
        >>> )
        >>>
        >>> # Plain DataFrame Containing Values
        >>> sa.df
        >>>
        >>> # Styled DataFrame
        >>> sa.styled_dfs()
        >>>
        >>> # Hex-Bin Plot
        >>> sa.plot()
    """
    sensitivity_values: Dict[str, Any]
    func: Callable

    result_name: str = 'Result'
    agg_func: Callable = np.mean
    reverse_colors: bool = False
    grid_size: int = 8
    func_kwargs_dict: Optional[Dict[str, Any]] = None
    num_fmt: Optional[str] = None
    color_map: str = 'RdYlGn'
    labels: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.func_kwargs_dict is None:
            self.func_kwargs_dict = {}
        self.df = sensitivity_df(
            self.sensitivity_values,
            self.func,
            result_name=self.result_name,
            labels=self.labels,
            **self.func_kwargs_dict
        )

    def plot(self, **kwargs) -> plt.Figure:
        """
        Creates hex-bin plots of the sensitivity analysis results

        :param kwargs: agg_func, reverse_colors, grid_size, color_map (see :py:class:`.SensitivityAnalyzer`)
        :return: Matplotlib Figure containing one or more plots of sensitivity analysis results
        """
        config_dict: Dict[str, Any] = dict(
            agg_func=self.agg_func,
            reverse_colors=self.reverse_colors,
            grid_size=self.grid_size,
            color_map=self.color_map,
        )
        config_dict.update(**kwargs)
        sensitivity_cols = self.sensitivity_cols
        return _hex_figure_from_sensitivity_df(
            self.df,
            sensitivity_cols,
            result_name=self.result_name,
            **config_dict
        )

    def styled_dfs(self, disp: bool = True, **kwargs) -> Union[Styler, Dict[Sequence[str], Styler]]:
        """
        Creates Pandas Styler objects showing a gradient over the sensitivity results

        :param disp: Whether to display the Styler objects before returning
        :param kwargs: reverse_colors, agg_func, num_fmt, color_map (see :py:class:`.SensitivityAnalyzer`)
        :return:
        """
        output = {}
        config_dict: Dict[str, Any] = dict(
            reverse_colors=self.reverse_colors,
            agg_func=self.agg_func,
            num_fmt=self.num_fmt,
            color_map=self.color_map,
        )
        config_dict.update(**kwargs)
        # Output a single Styler if only one or two variables
        sensitivity_cols = self.sensitivity_cols
        if len(sensitivity_cols) == 1:
            output[tuple(sensitivity_cols)] = _style_sensitivity_df(
                self.df,
                sensitivity_cols[0],
                reverse_colors=config_dict['reverse_colors'],
                col_subset=[self.result_name],
                result_col=self.result_name,
                num_fmt=config_dict['num_fmt'],
                color_map=config_dict['color_map'],
            )
        elif len(sensitivity_cols) == 2:
            col1 = sensitivity_cols[0]
            col2 = sensitivity_cols[1]
            df = _two_variable_sensitivity_display_df(
                self.df,
                col1,
                col2,
                result_col=self.result_name,
                agg_func=config_dict['agg_func']
            )
            output[(col1, col2)] = _style_sensitivity_df(
                df,
                col1,
                col2=col2,
                reverse_colors=config_dict['reverse_colors'],
                result_col=self.result_name,
                num_fmt=config_dict['num_fmt'],
                color_map=config_dict['color_map'],
            )
        elif len(sensitivity_cols) > 2:
            # Need to output multiple, one for each pair of variables
            for col1, col2 in itertools.combinations(sensitivity_cols, 2):
                df = _two_variable_sensitivity_display_df(
                    self.df,
                    col1,
                    col2,
                    result_col=self.result_name
                )
                output[(col1, col2)] = (_style_sensitivity_df(
                    df,
                    col1,
                    col2=col2,
                    reverse_colors=config_dict['reverse_colors'],
                    result_col=self.result_name,
                    num_fmt=config_dict['num_fmt'],
                    color_map=config_dict['color_map'],
                ))
        elif len(sensitivity_cols) == 0:
            raise ValueError('must pass sensitivity columns')

        if disp:
            for var_tup, sens_df in output.items():
                var_str = ' vs. '.join(var_tup)
                title_str = f'{self.result_name} by {var_str}'
                _display_header(title_str)
                display(HTML(sens_df.to_html()))

        if len(output) == 1:
            return list(output.values())[0]  # get Styler object out of dictionary

        return output

    @property
    def sensitivity_cols(self) -> List[str]:
        sensitivity_cols = list(self.sensitivity_values.keys())
        if self.labels:
            new_sensitivity_cols: List[str] = []
            for col in sensitivity_cols:
                if col in self.labels:
                    new_sensitivity_cols.append(self.labels[col])
                else:
                    new_sensitivity_cols.append(col)
            sensitivity_cols = new_sensitivity_cols
        return sensitivity_cols


def _display_header(text: str):
    html_str = f'<h2>{text}</h2>'
    display(HTML(html_str))