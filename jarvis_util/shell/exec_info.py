from enum import Enum
from jarvis_util.util.hostfile import Hostfile
import copy
import os
from abc import ABC, abstractmethod


class ExecType(Enum):
    LOCAL = 'LOCAL'
    SSH = 'SSH'
    PSSH = 'PSSH'
    MPI = 'MPI'


class ExecInfo:
    def __init__(self,  exec_type=ExecType.LOCAL, nprocs=None, ppn=None,
                 user=None, pkey=None, port=None, hostfile=None, env=None,
                 remote_env=None, sleep_ms=0, sudo=False, cwd=None, hosts=None,
                 collect_output=None, hide_output=None, file_output=None,
                 exec_async=False, stdin=None):
        self.exec_type = exec_type
        self.nprocs = nprocs
        self.user = user
        self.pkey = pkey
        self.port = port
        self.ppn = ppn
        self.hostfile = hostfile
        self._set_hostfile(hostfile=hostfile, hosts=hosts)
        self.env = env
        self.remote_env = remote_env
        self._set_env()
        self.cwd = cwd
        self.sudo = sudo
        self.sleep_ms = sleep_ms
        self.collect_output = collect_output
        self.file_output = file_output
        self.hide_output = hide_output
        self.exec_async = exec_async
        self.stdin = stdin

    def _set_env(self, env, remote_env):
        if env is None:
            self.env = {}
        if remote_env is None:
            self.remote_env = {}
        for key, val in os.environ.items():
            if key not in os.environ:
                self.env[key] = val
        for key, val in self.env.items():
            if key not in self.remote_env:
                self.remote_env[key] = val

    def _set_hostfile(self, hostfile=None, hosts=None):
        if hostfile is not None:
            if isinstance(hostfile, str):
                self.hostfile = Hostfile(hostfile=hostfile)
            elif isinstance(hostfile, Hostfile):
                self.hostfile = hostfile
            else:
                raise Exception("Hostfile is neither string nor Hostfile")
        if hosts is not None:
            if isinstance(hosts, list):
                self.hostfile = Hostfile(all_hosts=hosts)
            elif isinstance(hosts, str):
                self.hostfile = Hostfile(all_hosts=[hosts])
            elif isinstance(hosts, Hostfile):
                self.hostfile = hosts
            else:
                raise Exception("Host set is neither str, list or Hostfile")

        if hosts is not None and hostfile is not None:
            raise Exception("Must choose either hosts or hostfile, not both")

        if self.hostfile is None:
            self.hostfile = Hostfile()

    def mod(self, **kwargs):
        keys = ['exec_type', 'nprocs', 'ppn', 'user', 'pkey', 'port',
                'hostfile', 'env', 'remote_env', 'sleep_ms', 'sudo',
                'cwd', 'hosts', 'collect_output', 'hide_output',
                'file_output', 'exec_async', 'stdin']
        for key in keys:
            if key not in kwargs:
                kwargs[key] = getattr(self, key)
        return ExecInfo(**kwargs)

    def copy(self):
        return self.mod()


class Executable:
    def __init__(self):
        self.exit_code = None

    @abstractmethod
    def set_exit_code(self):
        pass

    @abstractmethod
    def wait(self):
        pass

