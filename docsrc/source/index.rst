.. sensitivity documentation master file, created by
   cookiecutter-pypi-sphinx.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Sensitivity Analysis documentation!
********************************************************************

Python Sensitivity Analysis - Gradient DataFrames and Hex-Bin Plots

To get started, look here.

.. toctree::
   :caption: Tutorial

   tutorial
   auto_examples/index

An overview
===========

Quick Links
------------

Find the source code `on Github <https://github.com/nickderobertis/sensitivity>`_.


sensitivity
-------------------------------------------------------


This is a simple example:

.. code:: python

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


.. toctree:: api/modules
   :caption: API Documentation
   :maxdepth: 3

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
