import warnings

def ignore_nested_library_warnings():
    warnings.filterwarnings("ignore", module="numpy.core.fromnumeric", category=FutureWarning)
    warnings.filterwarnings("ignore", module="pandas.io.formats.style", category=PendingDeprecationWarning, message="The get_cmap function will be deprecated in a future version")