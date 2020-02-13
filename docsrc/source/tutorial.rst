Getting started with sensitivity
**********************************

Install
=======

Install via::

    pip install sensitivity

Usage
=========

See more in the Example Usage section.

Simple usage::

    from sensitivity import SensitivityAnalyzer

    def my_model(x_1, x_2):
        return x_1 ** x_2

    sensitivity_dict = {
        'x_1': [10, 20, 30],
        'x_2': [1, 2, 3]
    }

    sa = SensitivityAnalyzer(sensitivity_dict, my_model)
    plot = sa.plot()
    styled_df = sa.styled_dfs()