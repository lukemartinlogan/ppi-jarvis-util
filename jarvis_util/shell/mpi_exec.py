from jarvis_util.shell.local_exec import LocalExec
from .exec_info import ExecInfo, ExecType


class MpiExec(LocalExec):
    def __init__(self, cmd, exec_info):
        self.cmd = cmd
        self.nprocs = exec_info.nprocs
        self.ppn = exec_info.ppn
        self.hostfile = exec_info.hostfile
        self.remote_env = exec_info.remote_env
        super().__init__(self.mpicmd(), exec_info)

    def mpicmd(self):
        params = [f"mpirun -n {self.nprocs}"]
        if self.ppn is not None:
            params.append(f"-ppn {self.ppn}")
        if len(self.hostfile):
            if self.hostfile.is_subset():
                params.append(f"--host {','.join(self.hostfile.hosts)}")
            else:
                params.append(f"--hostfile {self.hostfile.path}")
        params += [f"-genv {key}={val}" for key, val in self.remote_env.items()]
        params.append(self.cmd)
        cmd = " ".join(params)
        return cmd


class MpiExecInfo(ExecInfo):
    def __init__(self, **kwargs):
        super().__init__(exec_type=ExecType.MPI, **kwargs)
