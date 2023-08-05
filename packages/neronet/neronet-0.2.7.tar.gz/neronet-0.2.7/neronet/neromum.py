# -*- coding: utf-8 -*-
"""This module defines Neromum.
"""

# TODO: need database parsing

import os
import sys
import pickle
import glob
import time
import datetime
import shutil

import neronet.core
import neronet.daemon
import neronet.nerokid

class Neromum(neronet.daemon.Daemon):

    """A class to specify the Neromum object.

    Runs in the cluster and manages and monitors all the nodes.

    Gets the experiment as the 1st command line argument
    Experiment parameters from 2nd onwards.

    Attrs:
        exp_dict (dict): A dict of all experiments submitted to this mum by
            experiment ID.
        idling (bool): A boolean that tells if the daemon is idling.
        cluster (Cluster): The cluster object related to this server.
    """

    def __init__(self):
        super(Neromum, self).__init__('neromum')
        self.exp_dict = {}
        self.add_query('list_exps', self.qry_list_exps)
        self.add_query('exp_update', self.qry_exp_update)
        self.add_query('exp_set_warning', self.qry_exp_warning)
        self.add_query('input', self.qry_input)
        self.idling = False
        self.cluster = pickle.loads(neronet.core.read_file(os.path.join(
                neronet.core.USER_DATA_DIR_ABS, 'cluster.pickle')))
        self._host = self.cluster.ssh_address

    def qry_list_exps(self): # primarily for debugging
        """List all experiments submitted to this mum."""
        msg = 'Experiments:\n'
        for exp in self.exp_dict.values():
            msg += '- %s  %s  %s\n' % (exp.id, exp.state, exp.path)
        self._reply['msgbody'] = msg
        self._reply['rv'] = 0

    def qry_exp_update(self, exp_id, state, log_output):
        """Save information from Nerokids' experiment data updates."""
        exp = self.exp_dict[exp_id]
        # Extract log output update information
        for log_path, new_text in exp.log_output.items():
            # Initialize buffers for any new log path
            if log_path not in exp.log_output:
                exp.log_output[log_path] = ''
            # Append the new log output
            exp.log_output[log_path] += new_text
        # Update experiment state and timestamp
        exp.update_state(state)
        exp.time_modified = datetime.datetime.now()
        # Update the experiment pickle
        neronet.core.write_file(os.path.join(neronet.core.USER_DATA_DIR_ABS,
                'experiments', exp.id, 'exp.pickle'), pickle.dumps(exp))
        # Debugging
        if exp.state == neronet.core.Experiment.State.finished:
            self.log('Experiment "%s" has finished!' % (exp.id))
        self._reply['rv'] = 0
    
    def qry_exp_warning(self, exp_id, warnings):
        # FIXME is this function necessary? -Samuel
        exp = self.exp_dict[exp_id]
        exp.set_multiple_warnings(warnings)
        neronet.core.write_file(os.path.join(neronet.core.USER_DATA_DIR_ABS,
                'experiments', exp.id, 'exp.pickle'), pickle.dumps(exp))
        self._reply['rv'] = 0

    def qry_input(self, data):
        """Process input from Neroman."""
        now = datetime.datetime.now()
        answer = {}; msg = ''
        if 'action' in data:
            action = data['action']
            if action == 'clean_experiments':
                # Clean all experiments that have been either finished or
                # lost for at least 30 seconds
                exceptions = data['exceptions']
                experiments_cleaned_count = 0
                for exp_dir in glob.glob(os.path.join(neronet.core.USER_DATA_DIR_ABS,
                        'experiments/*')):
                    exp_id = os.path.basename(exp_dir)
                    # Skip deletion if not yet read or Neromun might have not
                    # fetched its results
                    if exp_id not in self.exp_dict or exp_id in exceptions:
                        continue
                    # Otherwise remove the directory
                    exp = self.exp_dict[exp_id]
                    self.log('Cleaning experiment "%s" (%s...' % (exp_id, exp.state))
                    shutil.rmtree(exp_dir)
                    del self.exp_dict[exp_id]
                    experiments_cleaned_count += 1
                msg += '%d experiments cleaned.\n' % (experiments_cleaned_count)
        self._reply['data'] = answer
        self._reply['msgbody'] = msg
        self._reply['rv'] = 0
    
    def ontimeout(self):
        """Load and start any unstarted received experiments."""
        # Load all experiments into the dict that have not yet been loaded
        for exp_file in glob.glob(os.path.join(neronet.core.USER_DATA_DIR_ABS,
                'experiments/*/exp.pickle')):
            #self.log('Checking exp "%s"...' % (exp_file))
            exp_id = os.path.basename(os.path.dirname(exp_file))
            if exp_id not in self.exp_dict:
                exp = pickle.loads(neronet.core.read_file(exp_file))
                self.log('New experiment detected: "%s" (%s)...' % (exp_id, exp.state))
                self.exp_dict[exp_id] = exp
        # Start an experiment if there is any to start
        for exp in self.exp_dict.values():
            if exp.state == neronet.core.Experiment.State.submitted_to_kid:
                pass
            elif exp.state == neronet.core.Experiment.State.submitted:
                # Initialize the log output container
                exp.log_output = {}
                # Launch experiment
                self.log('Launching experiment "%s"...' % (exp.id))
                if self.cluster.ctype == neronet.core.Cluster.Type.slurm:
                    exp_dir = os.path.join(neronet.core.USER_DATA_DIR_ABS,
                            'experiments', exp.id)
                    s = '#!/bin/bash\n'
                    s += '#SBATCH -J %s -D %s -o slurm.log\n' % (exp.id, exp_dir)
                    if self.cluster.sbatch_args: s += '#SBATCH %s\n' % (self.cluster.sbatch_args)
                    if exp.sbatch_args: s += '#SBATCH %s\n' % (exp.sbatch_args)
                    s += 'module load python/2.7.4\n'
                    s += 'nerokid %s --start; sleep 4;\n' % (exp.id)
                    s += 'nerokid %s --query configure %s %s; sleep 2m\n' % (exp.id, self._host, self._port)
                    #s += 'srun nerokid %s --query configure %s %s\n' % (exp.id, self._host, self._port)
                    sbatch_script = os.path.join(exp_dir, 'slurm.sh')
                    neronet.core.write_file(sbatch_script, s)
                    neronet.core.osrun('sbatch "%s"' % (sbatch_script))
                else:
                    # Launch experiment in the local (umanaged) node
                    nerokid = neronet.daemon.QueryInterface(neronet.nerokid.Nerokid(exp.id))
                    # Start the kid daemon
                    nerokid.start()
                    # Try to configure the kid
                    time.sleep(3.0)
                    nerokid.query('configure', host='localhost', port=self._port)
                # Update the experiment state and timestamp
                exp.update_state(neronet.core.Experiment.State.submitted_to_kid)
                exp.time_modified = now = datetime.datetime.now()
                return # pace submission by launching only one at a time
        # Compute the number of lost experiments
        lost_count = 0
        now = datetime.datetime.now()
        for exp in self.exp_dict.values():
            if exp.state in (neronet.core.Experiment.State.submitted_to_kid, neronet.core.Experiment.State.running) \
                    and exp.time_modified < now - datetime.timedelta(minutes=1):
                exp.update_state(neronet.core.Experiment.State.lost)
                lost_count += 1
        # Compute the number of finished experiments
        finished_count = 0
        for exp in self.exp_dict.values():
            if exp.state == neronet.core.Experiment.State.finished:
                finished_count += 1
        # Exit if all known (submitted) experiments are either finished or
        # lost and we've been idling for at least 5 minutes
        total_count = len(self.exp_dict)
        if finished_count + lost_count == total_count:
            if not self.idling:
                self.idling = True
                self.idling_since = now
            idling_duration = now - self.idling_since
            if idling_duration < datetime.timedelta(minutes=5):
                self.log('Nothing to do (%d/%d/%d). Idling for %s...' %
                        (lost_count, finished_count, total_count,
                        idling_duration))
            else:
                self.log('Quitting due to boredom...')
                self._doquit = True
        elif self.idling:
            self.idling = False

def main():
    """Create a CLI interface object and process CLI arguments."""
    cli = neronet.daemon.Cli(Neromum())
    cli.parse_arguments()

#if __name__ == '__main__':
#    main()
