"""
@file
@brief  Mock class @see cl TransferFTP

.. versionadded:: 1.0
    moved from pyensae to pyquickhelper
"""
from __future__ import unicode_literals

from ..loghelper.flog import noLOG
from .ftp_transfer import TransferFTP


class MockTransferFTP (TransferFTP):

    """
    mock @see cl TransferFTP
    """

    def __init__(self, site, login, password, fLOG=noLOG):
        """
        same signature as @see cl TransferFTP
        """
        self.LOG = fLOG
        self._atts = dict(site=site)

    def transfer(self, file, to, debug=False):
        """
        does nothing, returns True
        """
        return True

    def close(self):
        """
        does noting
        """
        pass
