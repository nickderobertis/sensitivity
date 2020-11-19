Overview of the sensitivity package
**************************************

Purpose
=======

It is common in financial modeling to conduct a sensitivity
analysis on the model. This analysis runs the model changing
the inputs values and collecting the outputs. Then the modeler
can examine how the outputs change in response to the inputs
changing. This library was created to ease this process,
especially around visualization of the results.

While it was developed for financial modeling, it can be used with
any function to understand how changing the inputs of the function
affect the outputs.

What Does it Do?
==================

The main logic of the ``SensitivityAnalyzer`` is replicating
a nested loop over the input values. Let's look at the basic
example of how to use ``SensitivityAnalyzer``::

    from sensitivity import SensitivityAnalyzer

    def my_model(x_1, x_2):
        return x_1 ** x_2

    sensitivity_dict = {
        'x_1': [10, 20, 30],
        'x_2': [1, 2, 3]
    }

    sa = SensitivityAnalyzer(sensitivity_dict, my_model)
    sa.df

This is roughly equivalent to::

    import pandas as pd

    def my_model(x_1, x_2):
        return x_1 ** x_2

    results = []
    for x_1 in [10, 20, 30]:
        for x_2 in [1, 2, 3]:
            res = my_model(x_1, x_2)
            results.append((x_1, x_2, res))
    df = pd.DataFrame(results, columns=['x_1', 'x_2', 'Result'])

The greater convenience comes with the built-in visualization::

    plot = sa.plot()
    styled_df = sa.styled_dfs()

Which handles generating hexbin plots and DataFrames with
a background gradient to signify high or low values.

What Happens with More Inputs?
================================

The hexbin plots and styled DataFrames can only display two
inputs changing at once, but it is possible to run
``SensitivityAnalyzer`` with as many inputs as you want.

To work with more than two inputs, ``SensitivityAnalyzer``
has two approaches: first, it displays as many hexbin plots
or styled DataFrames as needed to have the pairwise combinations
of the inputs. E.g. with inputs 1, 2, and 3, there would be three plots,
one for 1 and 2, one for 2 and 3, and one for 1 and 3. But even this
is not enough, because in that example, for each combination of 1 and 2,
there will be multiple results, one for each value of input 3. So
it is also necessary to aggregate the results to reach a single result
for the combination of the two inputs. ``SensitivityAnalyzer``
by default will take the mean, but it exposes the ``agg_func``
argument which should accept a list of values and return a single
value, so the user can pick any aggregation such as ``numpy``'s
``median`` or ``std`` function.