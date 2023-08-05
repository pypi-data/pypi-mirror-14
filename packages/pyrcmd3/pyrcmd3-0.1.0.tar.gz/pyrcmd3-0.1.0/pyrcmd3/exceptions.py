#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Pyrcmd3Exception(Exception):
    """Standard error for pyrcmd3 - Python Remote Command """
    pass


class AuthFailureException(Pyrcmd3Exception):
    """Exception : Client-> Server Problem with Authentication """
    pass


class BadHostKeyException(Pyrcmd3Exception):
    """Exception : Host Key does not match """
    pass


class SshProtocolException(Pyrcmd3Exception):
    """Exception : Problem of SSH2 Negotiation """
    pass


class TimeOutException(Pyrcmd3Exception):
    """Exception : Timeout while trying to connect to a valid address """
    pass


class TimeoutExecutingException(Pyrcmd3Exception):
    """Exception : Timeout while trying to execute command. """
    pass


class DNSLookupFailureException(Pyrcmd3Exception):
    """Exception : Error while trying to resolve name to IP. """
    pass
