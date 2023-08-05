"""
@file
@brief exceptions raised in this subfolder
"""
from __future__ import unicode_literals


class CoverageException(Exception):
    """
    raised when an issue happens with the coverage
    """
    pass


class SetupHookException(Exception):
    """
    raised when something happen while running setup_hook
    """
    pass
