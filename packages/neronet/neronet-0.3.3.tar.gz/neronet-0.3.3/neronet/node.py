import pickle

import neronet.core

class Node(object):
    """An object to represent nodes as used by Neronet

    Attributes:
        cid (str): The unique ID (name) of the node
        ctype (str): Type of the node. Either slurm or unmanaged
        ssh_address (str): SSH address or config hostname corresponding to
            the node.
        sbatch_args (str): Slurm SBATCH arguments.
    """


    class Type:
        """A simple class to represent the possible node types"""
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
        #self.experiment_count = 0    
    
    def sshrun(self, cmd, inp=None):
        """Execute a shell command via SSH on the remote Neronet node.

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
        # Potentially include initialization commands depending on node
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
            raise RuntimeError('Failed to run "%s" via SSH at node "%s"!%s'
                % (cmd, self.cid, msg))
        return res
        # PATH="$HOME/.neronet/neronet:/usr/local/bin:/usr/bin:/bin" PYTHONPATH="$HOME/.neronet"

    def test_connection(self):
        """A function to test connectivity to a node
        
        Raises:
            RuntimeError: 
        
        Returns:
            bool: True if successful"""
        try:
            res = self.sshrun('python -V')
        except RuntimeError:
            raise RuntimeError('Failed to run Python via SSH at "%s"!' % (self.cid))
        #TODO: Make version checking smarter
        if not 'Python 2.7' in res.err:
            raise RuntimeError('Incorrect Python version at "%s": "%s"!' % (self.cid, res.err))
        return True

    def gather_resource_info(self):
        #Gather node resource information in a dictionary
        results = {}
        try:
            info = self.sshrun('uptime; free -m; df -k .').out.split('\n')
        except RuntimeError:
            return {avgload: None, totalmem: None, usedmem: None, totaldiskspace:None, useddiskspace: None, percentagediskspace: None}
        results['avgload'] = info[0].split()[-1].replace(',', '.')
        memoryusage = info[2].split()
        results['totalmem'] = memoryusage[1]
        results['usedmem'] = memoryusage[2]
        diskspace = info[6].split()
        results['totaldiskspace'] = diskspace[1]
        results['useddiskspace'] = diskspace[2]
        results['percentagediskspace'] = diskspace[4]
        return results

    def start_neromum(self):
        res = self.sshrun('neromum --start')

    def clean_experiments(self, exceptions):
        data = {'action': 'clean_experiments', 'exceptions': exceptions}
        res = self.sshrun('neromum --input', inp=pickle.dumps(data, -1))
        print(res.out)
        if res.err:
            print('Error: %s\n' % (res.err))
    
    def terminate_exp(self, exp_id):
        data = {'action': 'terminate_exp', 'exp_id': exp_id}
        res = self.sshrun('neromum --input', inp=pickle.dumps(data, -1))
        print(res.out)
        if res.err:
            print('Error: %s\n' % (res.err))

    def yield_status(self):
        data = {'action': 'fetch', 'msg': 'I love honeybees!'}
        res = self.sshrun('neromum --input', inp=pickle.dumps(data, -1))
        yield 'Finished: %d, "%s", "%s"' % (res.rv, res.err, res.out)
