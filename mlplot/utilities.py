"""Common code to make writing plotting functions easier"""
from functools import wraps

import matplotlib.pyplot as plt
import numpy as np

# TODO add returns

DOCSTRING_HEADER = """\
Parameters
----------
"""

DOCSTRING_CLASSIFICATION_PARAMETERS = """\
y_true  : np.array
          A vector of size N that contains the true labels.
          There should be two labels of type string or numeric.
y_pred  : np.array
          A vector of size N that contains predictions as floats from 0 to 1.
labels  : dict, optional
          A dictionary mapping from lables in y_true to class names.
          Ex: {0: 'not dog', 1: 'is dog'}
ax      : matplotlib.axes.Axes, optional
"""

def classification_args(func):
    """
    Wrap func and provide the default classification arguments.

    This wrapper updates docstrings and places arguments at the front of
    the function definition.

    Parameters
    ----------
    func : function
           A classification plotting function
    """
    @wraps(func)
    def wrapper(y_true, y_pred, labels=None, ax=None, **kwargs):
        """Add default arguments and update the docstring"""
        try:
            y_true, y_pred, labels = validate_classification_arguments(y_true, y_pred, labels)
            ax = get_matplotlib_ax(ax)
        except AssertionError as err:
            # Raise more appropriate exception
            raise ValueError(err)

        func(y_true, y_pred, labels, ax, **kwargs)
        return ax

    # Update the docstring
    wrapper.__doc__ = add_docstring_parameters(wrapper.__doc__, DOCSTRING_CLASSIFICATION_PARAMETERS)

    return wrapper


def get_matplotlib_ax(ax):
    """Validate matplotlib axes or generate one if not provided"""
    if ax:
        assert isinstance(ax, plt.axes.Axes), 'You must pass a valid matplotlib.axes.Axes'
    else:
        _, ax = plt.subplots()
    return ax


def to_np_array(iterable, name):
    """Convert an iterable to a 1D numpy array or raise an error if not possible"""
    try:
        return np.array(iterable).ravel()
    except:
        raise AssertionError(f'Cannot convert {name} to numpy array')


# TODO cleanup
def validate_classification_arguments(y_true, y_pred, labels):
    """Validate arguments for classification plots and return the cleaned-up arguments"""
    # Convert iterable to numpy array
    y_true = to_np_array(y_true, 'y_true')
    y_pred = to_np_array(y_pred, 'y_pred')

    # Check that y_true and y_pred meet the requirements
    assert len(y_true.shape) == 1, 'y_true must by 1D'
    assert len(y_pred.shape) == 1, 'y_pred must by 1D'
    assert y_true.shape == y_pred.shape, 'y_true and y_pred must be the same length'

    # Ensure that there are only 2 classes and convert all values to 0/1
    values = np.unique(y_true)
    assert len(values) == 2, 'y_true should have 2 values'
    values_map = {0.0: values[0], 1.0: values[1]}
    y_true[y_true == values[0]] = 0.0
    y_true[y_true == values[1]] = 1.0

    # Validate and update the labels map
    if labels:
        assert len(labels) == 2, 'Labels mapping should have only 2 classes'
        assert set(labels.keys()) == set(values), f'Labels mapping should have keys for all values ({values})'
        labels = {val: labels[lbl] for val, lbl in values_map.items()}
    else:
        labels = values_map

    # Ensure y_pred has numeric values between 0.0-1.0
    assert np.issubdtype(y_pred.dtype, np.number), 'y_pred must contain numeric types'
    y_pred = y_pred.astype(float)
    assert np.all(0.0 <= y_pred) and np.all(y_pred <= 1.0), 'y_pred must contain values between 0.0 and 1.0 inclusive'

    # TODO namedtuple
    return y_true, y_pred, labels


def add_docstring_parameters(doc, parameters, header=DOCSTRING_HEADER):
    """Update and return the docstring of a function by adding the parameters string following numpy convention."""
    assert doc, 'Docstring required'

    # Remove leading whitespace
    lines = doc.expandtabs().splitlines()
    lines[0] = lines[0].strip()  # First line should have no spacing
    if len(lines) > 1:
        indent = min([len(ln) - len(ln.lstrip()) for ln in lines[1:] if len(ln)])
        lines[1:] = [ln[indent:] for ln in lines[1:]]
    lines = [ln.rstrip() for ln in lines]
    doc = '\n'.join(lines)

    # Add new parameter docstring
    new_params = header + parameters
    if header in doc:
        # Add parameters to docstring
        doc = doc.replace(header, new_params)
    else:
        # Assume no parameters written
        doc += '\n\n' + new_params

    return doc
