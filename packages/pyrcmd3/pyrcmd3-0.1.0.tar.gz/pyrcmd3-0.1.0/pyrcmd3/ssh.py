#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import content

import paramiko
from pyrcmd3.exceptions import AuthFailureException
from pyrcmd3.exceptions import BadHostKeyException
from pyrcmd3.exceptions import DNSLookupFailureException
from pyrcmd3.exceptions import SshProtocolException
from pyrcmd3.exceptions import TimeOutException
from pyrcmd3.exceptions import TimeoutExecutingException
import socket
import time


class SSH(object):
    """Connect and execute command to a client server

        Attributes:

        Address     IP or Hostname to client server
        User        User used to connect using ssh
        passwd      Password used to connect to ssh
        timeout     Timeout to Connect (Hostname is valid and has route to
                    host), default value for timeout is 30

        Return:     Dictionary (Array) with Return Code, Std output and Std
                    Error

        Exceptions: AuthFailureException : Client-> Server Problem with
                                            Authentication
                    BadHostKeyException: Host Key does not match
                    SshProtocolException: Problem of SSH2 Negotiation
                    TimeOutException: Timeout while trying to connect to a
                    valid address
                    TimeoutExecutingException: Timeout while trying to execute
                    command.
                    DNSLookupFailureException: Error while trying to resolve
                    name to IP.
    """

    def __init__(self, address, user, passwd, timeout=30):
        self.address = address
        self.user = user
        self.passwd = passwd
        self.timeout = timeout

    def execute(self, command):
        global client
        seconds_to_timeout = 1
        try:
            socket.gethostbyname(self.address)
        except socket.gaierror:
            raise DNSLookupFailureException(
                "DNS Lookup Failure to address: %r" % self.address)

        while True:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                client.connect(self.address, username=self.user,
                               password=self.passwd, timeout=self.timeout)
                break
            except paramiko.AuthenticationException as e:
                raise AuthFailureException(e) from None
            except paramiko.BadHostKeyException as e:
                raise BadHostKeyException(e) from None
            except paramiko.SSHException as e:
                raise SshProtocolException(e) from None
            except socket.timeout:
                raise TimeOutException(
                    "Timeout while trying to connect to a valid "
                    "address.") from None
            except Exception:
                seconds_to_timeout += 1
                time.sleep(1)

            if seconds_to_timeout == 15:
                raise TimeoutExecutingException(
                    "Timeout while trying to execute command.") from None

        command_response = {'return_code': '', 'stdout': '', 'stderr': ''}
        chan = client.get_transport().open_session()
        chan.settimeout(self.timeout)
        chan.exec_command(command=command)
        command_response['return_code'] = chan.recv_exit_status()

        while chan.recv_ready():
            command_response['stdout'] += str(chan.recv(1024))

        while chan.recv_stderr_ready():
            command_response['stderr'] += str(chan.recv_stderr(1024))

        client.close()

        return command_response
