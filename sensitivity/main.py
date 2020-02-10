import itertools
from dataclasses import dataclass
from typing import Dict, Any, Callable, Optional, List, Union

import numpy as np
from pandas.io.formats.style import Styler
import matplotlib.pyplot as plt

from sensitivity.df import sensitivity_df, _style_sensitivity_df, _two_variable_sensitivity_display_df
from sensitivity.hexbin import sensitivity_hex_plots, _hex_figure_from_sensitivity_df


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
        >>> sa.styled_dfs
        >>>
        >>> # Hex-Bin Plot
        >>> sa.plot
    """
    sensitivity_values: Dict[str, Any]
    func: Callable

    result_name: str = 'Result'
    agg_func: Callable = np.mean
    reverse_colors: bool = False
    grid_size: int = 8
    func_kwargs_dict: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.func_kwargs_dict is None:
            self.func_kwargs_dict = {}
        self.df = sensitivity_df(
            self.sensitivity_values,
            self.func,
            result_name=self.result_name,
            **self.func_kwargs_dict
        )

    @property
    def plot(self) -> plt.Figure:
        sensitivity_cols = list(self.sensitivity_values.keys())
        return _hex_figure_from_sensitivity_df(
            self.df,
            sensitivity_cols,
            result_name=self.result_name,
            agg_func=self.agg_func,
            reverse_colors=self.reverse_colors,
            grid_size=self.grid_size
        )

    @property
    def styled_dfs(self) -> Union[Styler, List[Styler]]:
        # Output a single Styler if only one or two variables
        sensitivity_cols = list(self.sensitivity_values.keys())
        if len(sensitivity_cols) == 1:
            return _style_sensitivity_df(
                self.df,
                sensitivity_cols[0],
                reverse_colors=self.reverse_colors,
                col_subset=[self.result_name],
                result_col=self.result_name
            )
        elif len(sensitivity_cols) == 2:
            col1 = sensitivity_cols[0]
            col2 = sensitivity_cols[1]
            df = _two_variable_sensitivity_display_df(
                self.df,
                col1,
                col2,
                result_col=self.result_name
            )
            return _style_sensitivity_df(
                df,
                col1,
                col2=col2,
                reverse_colors=self.reverse_colors,
                result_col=self.result_name,
            )
        elif len(sensitivity_cols) == 0:
            raise ValueError('must pass sensitivity columns')

        # Length must be greater than 2, need to output multiple, one for each pair of variables
        results = []
        for col1, col2 in itertools.combinations(sensitivity_cols, 2):
            df = _two_variable_sensitivity_display_df(
                self.df,
                col1,
                col2,
                result_col=self.result_name
            )
            results.append(_style_sensitivity_df(
                df,
                col1,
                col2=col2,
                reverse_colors=self.reverse_colors,
                result_col=self.result_name,
            ))
        return results