# -*- coding: utf-8 -*-
"""This module defines Nerokid.

Attributes:
  INTERVAL (float): interval for how long the kid waits until it rechecks
    for changes in the log file
  LOG_FILES (tuple): Log files for stdout and stderr

Example usage:
    ## Unmanaged node example
    python nerokid exp1 --start
    ## Managed node example (Slurm SBATCH)
    #!/bin/sh
    #SBATCH --time=60
    python nerokid exp1 --start
    python nerokid exp1 --launch triton 12345
"""

from __future__ import print_function
import os
import subprocess
import shlex
import time
import sys
import pickle

import neronet.core
import neronet.daemon
import neronet.neromum

INTERVAL = 2.0
commands = ("status")

class LogFile(object):

    """A class that facilitates efficient monitoring of logfile changes."""

    def __init__(self, path):
        """Create a LogFile object to represent a log file.

        Args:
            path (str): the file path to the log file.
        """
        self.path = path
        self.rtime = 0
        self.seek = 0

    def read_changes(self):
        """Return changes made to the logfile as a single string."""
        mtime = os.stat(self.path).st_mtime
        if mtime > self.rtime:
            self.rtime = mtime
            with open(self.path, 'r') as stream:
                stream.seek(self.seek)
                changes = stream.read()
                self.seek = stream.tell()
                return changes


class Nerokid(neronet.daemon.Daemon):

    """A class to specify the Nerokid object.

    Runs in a cluster node and manages and monitors the experiment given.

    Gets host as the 1st command line argument
    Port as the 2nd
    Experiment as the 3rd
    Experiment parameters from 4th argument onwards
    """
    def __init__(self, exp_id):
        super(Nerokid, self).__init__('nerokid-%s' % (exp_id))
        self.neromum = None
        self.exp_id = exp_id
        self.exp = None
        self.process = None
        self.add_query('configure', self.qry_configure)

    def qry_configure(self, host, port):
        """Connect with Neromum.

        Initializes the query interface.
        """
        self.neromum = neronet.daemon.QueryInterface(
                neronet.neromum.Neromum(), host=host, port=int(port))
        self.log('Mom address: (%s, %d)' % (self.neromum.host,
                self.neromum.port))
        self._reply['rv'] = 0

    def qry_stop(self):
        """Terminate the experiment"""
        if self.process and self.process.poll() == None:
            self.log('Killing the experiment...')
            self.process.kill()
        super(Nerokid, self).qry_stop()

    def ontimeout(self):
        """Writes information about the process into a log file on set intervals"""
        # If the experiment is defined and running
        if self.exp and self.exp.state == neronet.core.Experiment.State.running:
            # Collect any data that the child process has output
            log_output = {}
            terminated = False
            for log_file in self.log_files:
                if not os.path.exists(log_file.path):
                    self.log('No output file %s!' % (log_file.path))
                    continue
                changes = log_file.read_changes()
                if changes:                   
                    rows = changes.split('\n')
                    for row in rows:
                        result = self.exp.get_action(row)
                        if result[0] == 'kill':
                            self.exp.update_state(neronet.core.Experiment.State.terminated)
                            self.log('Termination condition ' + result[1] + ' was met. The experiment will be terminated.')
                            self.qry_stop()
                            terminated = True
                            changes += '\nTermination condition \'' + result[1] + '\' was met. The experiment will be terminated.\n'
                        elif result[0] == 'warn' and not terminated:
                            self.exp.set_warning(result[1])
                            changes += '\nWARNING: condition ' + result[1] + ' was met.\n'
                            self.log('WARNING: condition ' + result[1] + ' was met.')
                            # FIXME: This data would end up there anyway via next update -Samuel
                            self.neromum.query('exp_set_warning', self.exp_id,
                                self.exp.get_warnings())
                    log_output[log_file.path[len(self.exp_dir)+1:]] = changes
            # If the process has stopped
            if self.process.poll() != None and terminated == False:
                self.log('Experiment has finished!')
                self.exp.update_state(neronet.core.Experiment.State.finished)
                # Flag the daemon for exit
                self.qry_stop()
            # Send any information to Neromum
            try:
                self.log('Updating Neromum...')
                self.log('Query: %s, (%s, %s out: %s)' % ('exp_update',
                        self.exp_id, self.exp.state, log_output))
                self.neromum.query('exp_update', self.exp_id,
                        self.exp.state, log_output)
            except RuntimeError as err:
                self.err('Cannot communicate with Neromum!', err)
        # If the experiment is not defined and we have Neromum defined, start
        # the experiment!
        elif not self.exp and self.neromum:
            """Launches received script"""
            # Load the experiment data
            self.log('Loading the experiment object...')
            self.exp_dir = os.path.join(neronet.core.USER_DATA_DIR_ABS,
                    'experiments', self.exp_id)
            self.exp = pickle.loads(neronet.core.read_file(os.path.join(
                    self.exp_dir, 'exp.pickle')))
            self.log('Experiment ID: "%s"' % (self.exp.id))
            self.log_files = [LogFile(os.path.join(self.exp_dir,
                    log_file_path)) for log_file_path in ('stdout.log',
                    'stderr.log')]
            self.log('Launching the experiment...')
            # Change temprarily to the experiment's directory and launch the
            # experiment there
            cwd = os.getcwd()
            os.chdir(self.exp_dir)
            self.process = subprocess.Popen(
                shlex.split(self.exp.callstring),
                universal_newlines=True,
                stdout=open('stdout.log', 'w'),
                stderr=open('stderr.log', 'w'),
                close_fds=True, bufsize=1)
            os.chdir(cwd)
            self.log('Experiment PID: %s' % (self.process.pid))
            self.exp.update_state(neronet.core.Experiment.State.running)

def main():
    """Create a CLI interface object and process CLI arguments."""
    if len(sys.argv) < 2:
        print('Kid experiment ID required!')
        sys.exit(1)
    exp_id = sys.argv[1]
    sys.argv.pop(1)
    #sys.argv = [sys.argv[0]] + sys.argv[2:]
    cli = neronet.daemon.Cli(Nerokid(exp_id))
    cli.parse_arguments()

#if __name__ == '__main__':
#    main()
