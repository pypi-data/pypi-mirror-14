"""
@file
@brief Some automation helpers about notebooks
"""
from __future__ import unicode_literals


class NotebookException(Exception):

    """
    Exception raises when something wrong happened with a notebook.
    """
    pass


class InNotebookException(Exception):

    """
    Exception raises when something wrong happened in a notebook.

    .. versionadded:: 1.3
    """
    pass


class JupyterException(Exception):

    """
    Exception raises by Jupyter

    .. versionadded:: 1.3
    """
    pass
