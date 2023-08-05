import pickle

import neronet.core

class Cluster(object):
    """An object to represent clusters as used by Neronet

    

    Attributes:
        cid (str): The unique ID (name) of the cluster
        ctype (str): Type of the cluster. Either slurm or unmanaged
        ssh_address (str): SSH address or config hostname corresponding to
            the cluster.
        sbatch_args (str): Slurm SBATCH arguments.
    """

    class Type:
        """A simple class to represent the possible cluster types"""
        unmanaged = 'unmanaged'
        slurm = 'slurm'
        _members = set(['slurm', 'unmanaged'])

        @classmethod
        def is_member(cls, arg):
            return arg in cls._members

    def __init__(self, cid, ctype, ssh_address, sbatch_args=None, \
                usr_dir=neronet.core.USER_DATA_DIR):
        self.cid = cid
        self.ctype = ctype
        self.ssh_address = ssh_address
        self.sbatch_args = sbatch_args
        self.dir = usr_dir

    def __str__(self):
        return '%s (%s, %s)' % (self.cid, self.ctype, self.ssh_address)

    def sshrun(self, cmd, inp=None):
        """Execute a shell command via SSH on the remote Neronet cluster.

        To ensure that Neronet commands can be run with this function,
        the given command 'cmd' is preceded by a few bash commands
        to set up the correct Python environment.

        Returns:
            Runresult: An object containing the 
            result of running the command"""
        # Ask SSH to execute a command that starts by changing the working
        # directory to 'self.dir' at the machine served at the specified
        # address and port
        scmd = 'ssh %s "cd %s;' % (self.ssh_address, self.dir)
        # Potentially include initialization commands depending on cluster
        # type
        if self.ctype == self.Type.unmanaged:
            pass
        elif self.ctype == self.Type.slurm:
            # Load the python 2.7 module to gain access to the interpreter
            scmd += ' module load python/2.7.4;'
        # Run the given command with the PATH and PYTHONPATH environment
        # variables defined to include the neronet executables and modules
        scmd += ' PATH="%s/neronet:/usr/local/bin:/usr/bin:/bin" PYTHONPATH="%s" %s"' \
                % (self.dir, self.dir, cmd)
        # Actual execution
        res = neronet.core.osrunroe(scmd, inp=inp)
        if res.rv != 0:
            msg = ''
            if res.err: msg += '\nErr: %s' % (res.err)
            if res.out: msg += '\nOut: %s' % (res.out)
            raise RuntimeError('Failed to run "%s" via SSH at cluster "%s"!%s'
                % (cmd, self.cid, msg))
        return res
        # PATH="$HOME/.neronet/neronet:/usr/local/bin:/usr/bin:/bin" PYTHONPATH="$HOME/.neronet"

    def test_connection(self):
        """A function to test connectivity to a cluster
        
        Raises:
            RuntimeError: 
        
        Returns:
            bool: True if successful"""
        res = self.sshrun('python -V')
        if res.rv != 0:
            raise RuntimeError('Failed to run Python via SSH at "%s"!' % (self.cid))
        #TODO: Make version checking smarter
        elif not 'Python 2.7' in res.err:
            raise RuntimeError('Incorrect Python version at "%s": "%s"!' % (self.cid, res.err))
        return True

    def start_neromum(self):
        res = self.sshrun('neromum --start')
        print('Neromum daemon started...')
        #print('Finished: %d, "%s", "%s"' % (res.rv, res.err, res.out))

    def clean_experiments(self, exceptions):
        data = {'action': 'clean_experiments', 'exceptions': exceptions}
        res = self.sshrun('neromum --input', inp=pickle.dumps(data, -1))
        print(res.out)
        if res.err:
            print('Error: %s\n' % (res.err))

    def yield_status(self):
        data = {'action': 'fetch', 'msg': 'I love honeybees!'}
        res = self.sshrun('neromum --input', inp=pickle.dumps(data, -1))
        yield 'Finished: %d, "%s", "%s"' % (res.rv, res.err, res.out)


