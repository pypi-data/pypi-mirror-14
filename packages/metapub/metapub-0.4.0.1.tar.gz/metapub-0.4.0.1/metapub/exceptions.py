from __future__ import absolute_import, unicode_literals

from lxml.etree import XMLSyntaxError
from eutils.exceptions import *

class MetaPubError(Exception):
    pass

class InvalidPMID(MetaPubError):
    """Raised when NCBI efetch of a pubmed ID results in "invalid" response."""

class CrossRefConnectionError(MetaPubError):
    """Raised when a well-formed CrossRef query results in a server error."""

class NoPDFLink(MetaPubError):
    """Raised when a FindIt url lookup fails for some specific reason that is
    particular to the journal or publisher.

    This Exception provides extended attributes:

            reason      :    human-readable "reason" why URL lookup failed.
            url         :    last url attempted 
            status_code :    last HTTP code returned in attempt (if any)
            missing     :    list of data items missing from last attempt (if any)

    This Exception is mostly used internally in FindIt as flow control.
    """
    def __init__(self, reason, *args, **kwargs):
        self.message = reason
        self.reason = reason
        self.url = kwargs.get('url', None)
        self.missing = kwargs.get('missing', [])
        self.status_code = kwargs.get('status_code', None)

        super(NoPDFLink, self).__init__(reason, *args, **kwargs) 

class AccessDenied(NoPDFLink):
    """Raised when a FindIt url lookup fails for some specific reason that is
    particular to the journal or publisher."""

class BadDOI(MetaPubError):
    """Raised when DxDOI class tests validity of DOI and it fails to pass muster."""

class DxDOIError(MetaPubError):
    """Raised when a bad status code comes from loading dx.doi.org"""


