from typing import Dict, Any, Callable, Sequence
import itertools
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

from sensitivity.colors import _get_color_map
from sensitivity.df import sensitivity_df


def sensitivity_hex_plots(sensitivity_values: Dict[str, Any], func: Callable,
                          result_name: str = 'Result', agg_func: Callable = np.mean,
                          reverse_colors: bool = False, grid_size: int = 8,
                          color_map: str = 'RdYlGn',
                          **func_kwargs) -> plt.Figure:
    """
    Create hexbin plots showing how the func result varies with a passed dictionary of input values.
    Automatically creates a plot for each pair of input parameters passed.

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
    :param color_map: matplotlib color map, default is RdYlGn (red, yellow, green). See
        https://matplotlib.org/3.3.2/tutorials/colors/colormaps.html
    :param func_kwargs: Additional arguments to pass to func, regardless of the sensitivity values picked
    :return: Sensitivity analysis hex bin sub plot figure
    """
    s_df = sensitivity_df(
        sensitivity_values,
        func,
        result_name=result_name,
        **func_kwargs
    )
    sensitivity_cols = list(sensitivity_values.keys())
    return _hex_figure_from_sensitivity_df(
        s_df,
        sensitivity_cols,
        result_name=result_name,
        agg_func=agg_func,
        reverse_colors=reverse_colors,
        grid_size=grid_size,
        color_map=color_map,
    )


def _hex_figure_from_sensitivity_df(df: pd.DataFrame, sensitivity_cols: Sequence[str],
                                    result_name: str = 'Result', agg_func: Callable = np.mean,
                                    reverse_colors: bool = False, grid_size: int = 8,
                                    color_map: str = 'RdYlGn') -> plt.Figure:
    color_str = _get_color_map(reverse_colors=reverse_colors, color_map=color_map)
    combos = list(itertools.combinations(sensitivity_cols, 2))
    num_columns = 3
    num_rows = int(math.ceil(len(combos) / num_columns))
    gs = GridSpec(num_rows, num_columns)
    fig = plt.figure(figsize=(15, 4 * num_rows))
    for i, (x, y) in enumerate(combos):
        ax = fig.add_subplot(gs[i])
        hb = ax.hexbin(x=df[x],
                       y=df[y],
                       C=df[result_name],
                       reduce_C_function=agg_func,
                       gridsize=grid_size,
                       cmap=color_str)
        plt.xlabel(x)
        plt.ylabel(y)
        cb = fig.colorbar(hb, ax=ax)
        cb.set_label(result_name)
    fig.tight_layout()
    return fig
