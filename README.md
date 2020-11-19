
[![](https://codecov.io/gh/nickderobertis/sensitivity/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/sensitivity)

# sensitivity

## Overview

Python Sensitivity Analysis - Gradient DataFrames and Hex-Bin Plots

It is common in financial modeling to conduct a sensitivity analysis on the model. This analysis runs the model changing the inputs values and collecting the outputs. Then the modeler can examine how the outputs change in response to the inputs changing. This library was created to ease this process, especially around visualization of the results.

While it was developed for financial modeling, it can be used with any function to understand how changing the inputs of the function affect the outputs.

## Getting Started

Install `sensitivity`:

```
pip install sensitivity
```

A simple example:

```python
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
```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/sensitivity/
)

## Author

Created by Nick DeRobertis. MIT License.