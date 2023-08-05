# -*- coding: utf-8 -*-
"""This module defines Neroman.

To work with Neroman each experiment must have the following attributes
defined in its config:

* experiment_id: The unique identifier for the experiment
* run_command_prefix: The run command of the experiment
* main_code_file: The code file to be run
* destination_folder: Folder that the experiment is run in on the cluster.
* parameters: The definition of the experiment parameters
* parameters_format: The format of the experiment parameters
* logoutput: The location the experiment outputs its output
* state: A tuple of the experiment state which is set to 'defined' by this
  function and the time changed
* cluster: The cluster that the experiment is running on. Set to
  None by this function
* time_created: Sets the current time as the creation time
* time_modified: The time the experiment was last modified. Sets
  this time to the same as the time created
* path: The absolute path to the folder

Attributes:
  CONFIG_FILENAME (str): The name of the config file inside the
    experiment folder that specifies the experiment.
"""

import os
import time
import yaml
import sys
import subprocess
import pickle

import neronet.core
import neronet.daemon

CONFIG_FOLDER = pathlib.Path.home() / '.neronet'
CONFIG_FILENAME = 'config.yaml'


class FormatError(Exception):
    """Exception raised when experiment config file is poorly formatted."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Neroman(neronet.daemon.Daemon):
    """The part of Neronet that handles user side things.

    Attributes:
        database_file (str): Path to the database used, currently only .yaml
        clusters (Dict): A dictionary containing the specified clusters
        experiments (Dict): A dictionary containing the specified experiments
        preferences (Dict): A dictionary containing the preferences
    """

    def __init__(self):
        """Initializes Neroman

        Reads the contents of its attributes from a database (currently just
        a .yaml file).

        Args:
            database_file (str): The path to the database file as a string,
                the rest of the attributes will be parsed from the database.
        """
        super().__init__('neroman')
        self.database_file = CONFIG_FOLDER / 'default.yaml'
        self.clusters_file = CONFIG_FOLDER / 'clusters.yaml'
        self.preferences_file = CONFIG_FOLDER / 'preferences.yaml'
        self.clusters = {}
        self.experiments = {}
        self.preferences = {}
        try:
            self._load_configurations()
        except neronet.neroman.FormatError as e:
            self.abort('Reading config files failed!', e)
        self.add_query('status', self.qry_status)
        self.add_query('specify_cluster', self.qry_specify_cluster)

    def _load_config(self, config_file, default=None):
        return yaml.load(config_file.read_text()) if config_file.exists() \
                else default

    def _save_config(self, config_file, data):
        """Save config data into the config file path."""
        config_file.write_text(yaml.dump(data, default_flow_style=False))

    def _load_configurations(self):
        """Load the configurations from the yaml files or creates them if they
        don't exist
        """
        self.preferences = self._load_config(self.preferences_file)
        if not self.preferences:
            self.preferences = {'name': None, 'email': None, 'default_cluster': None}
            self._save_config(self.preferences_file, self.preferences)

        self.clusters = self._load_config(self.clusters_file)
        if not self.clusters:
            self.clusters = {'clusters': {}, 'groups': None}
            self._save_config(self.clusters_file, self.clusters)

        self.experiments = self._load_config(self.database_file)
        if not self.experiments:
            self.experiments = {}
            self._save_config(self.database_file, self.experiments)

    def qry_status(self, arg=None):
        """Return status information."""
        if arg == None or arg == 'all':
            msg = '==> Neroman Status Report ==>\n'
            msg += '--> Clusters -->\n'
            if self.clusters['clusters']:
                for name, cluster in self.clusters['clusters'].items():
                    ssh_address = cluster['ssh_address']
                    cluster_type = cluster['type']
                    msg += '%s %s %s\n' % (name, ssh_address, cluster_type)
            else:
                msg += 'No clusters defined\n'
            msg += '--> Experiments -->\n'
            if self.experiments:
                for name, experiment in self.experiments.items():
                    msg += '%s: %s' % (name, experiment['state'].pop()[0])
            else:
                msg += 'No experiments defined\n'
        elif arg in self.experiments:
            msg = '==> Experiment Status Report ==>\n'
            experiment = self.experiments[arg]
            parameters = experiment['parameters']
            time_modified = experiment['time_modified']
            state, state_change_time = experiment['state'].pop()
            parameters_string = ', '.join(
                ["%s: %s" % (k, v) for k, v in parameters.items()])
            msg += 'Experiment: %s\nParameters: %s\n' % \
                    (arg, parameters_string)
            if state == 'defined':
                msg += 'State: %s - %s\n' % (state, state_change_time)
            else:
                cluster = experiment['cluster']
                msg += 'State: %s - %s - %s\n' % \
                    (state, cluster, state_change_time)
            msg += 'Last modified: %s\n' % (time_modified)
        else:
            raise IOError('No experiment named "%s"!' % (arg))
        self._reply['msgbody'] = msg
        self._reply['rv'] = 0

    def qry_specify_cluster(self, name, ssh_address, cluster_type, port=22):
        """Specify clusters so that Neroman is aware of them.

        Writes cluster name, address and type to the clusters config file

        Args:
            name (str): The name of the cluster, should be unique
            ssh_address (str): SSH address of the cluster
            cluster_type (str): Type of the cluster (slurm or unmanaged)
            port (int): SSH port number

        Raises:
            FormatError: if the cluster type isn't unmanaged or slurm
        """
        if cluster_type != 'slurm' and cluster_type != 'unmanaged':
            raise FormatError("Cluster type should be slurm or unmanaged")

        self.clusters['clusters'][name] = {
                'ssh_address': ssh_address,
                'type': cluster_type,
                'port': port}
        self._save_config(self.clusters_file, self.clusters)
        self._reply['rv'] = 0

    def qry_specify_experiments(self, folder):
        """Specify experiments so that Neroman is aware of them.

        Reads the contents of the experiment from a config file inside the
        specified folder.

        Args:
            folder (str): The path of the folder that includes
                the experiment that's being specified.

        Raises:
            FileNotFoundError: If the folder doesn't exists or the config file
                doesn't exists
            FormatError: If the config file is badly formated
        """
        folder = pathlib.Path(folder)
        if not folder.isdir():
            raise FileNotFoundError('No such folder!')
        config_file = folder / CONFIG_FILENAME
        if not config_file.exists():
            raise FileNotFoundError('No config file in folder!')
        if config_file.stat().st_size == 0:
            raise FormatError('Empty config file')
        experiment_data = self._load_config(config_file)
        experiment = {}
        for field in ['run_command_prefix', 'main_code_file',
                      'parameters', 'parameters_format', 'logoutput']:
            if field not in experiment_data:
                raise FormatError('No %s field in experiment' % (field))
            experiment[field] = experiment_data[field]
        experiment['cluster'] = None
        experiment['time_created'] = neronet.core.time_now()
        experiment['state'] = [('defined', experiment['time_created'])]
        experiment['time_modified'] = experiment['time_created']
        experiment['path'] = folder.abspath()
        if 'experiment_id' not in experiment_data:
            raise FormatError('No experiment_id field in experiment')
        else:
            self.experiments[experiment_data['experiment_id']] = experiment
        self._save_config(self.database_file, self.experiments)
        self._reply['rv'] = 0

    def qry_update_state(self, exp_id, state):
        self._update_state(exp_id, state)
        self._reply['rv'] = 0

    def _update_state(self, exp_id, state):
        self.experiments[exp_id]['state'].append((state,
                neronet.core.time_now()))

    def qry_submit(self, exp_id, cluster_id):
        """Submit and start the experiment in the cluster using ssh.

        Args:
            exp_id (str): the experiment ID
            cluster_id (str): the cluster ID
        """
        experiment = self.experiments[exp_id]
        cluster = self.clusters[cluster_id]
        remote_dir = pathlib.Path('/tmp/neronet-%d' % (time.time()))
        experiment_dir = experiment['path']
        experiment_results_dir = experiment_dir + "/" + experiment['logoutput']
        experiment_callstring = self._create_experiment_callstring(exp_id)
        experiment['cluster'] = cluster_id
        cluster_port = cluster['port']
        cluster_address = cluster['ssh_address']
        self._send_files(
            experiment_dir,
            remote_dir,
            cluster_address,
            cluster_port)
        # Magic do NOT touch:
        neronet.core.osrun(
            'ssh -p%s %s "cd %s; PATH="%s/bin:/usr/local/bin:/usr/bin:/bin" PYTHONPATH="%s" neromum %s"' %
            (cluster_port,
             cluster_address,
             remote_dir,
             remote_dir,
             remote_dir,
             experiment_callstring))
        self._update_state(exp_id, 'submitted')
        self._save_config(self.database_file, self.experiments)
        time.sleep(2)  # will be unnecessary as soon as daemon works
        # returns the results, should be called from cli
        self._get_experiment_results(exp_id, remote_dir, experiment_results_dir)

    def _create_experiment_callstring(self, experiment_id):
        if experiment_id not in self.experiments:
            raise IOError('No experiment named %s' % experiment_id)
        experiment = self.experiments[experiment_id]
        rcmd = experiment['run_command_prefix']
        code_file = experiment['main_code_file']
        params = experiment['parameters']
        pformat = experiment['parameters_format']
        pstr = pformat.format(**params)
        return ' '.join([rcmd, code_file, pstr])

    def _send_files(
            self,
            experiment_folder,
            remote_dir,
            cluster_address,
            cluster_port,
            neronet_root=pathlib.Path.cwd()):
        """Send experiment files to the cluster

        Args:
            experiment_folder (str): the file path to experiment folder on the local machine.
            remote_dir (str): the file path to experiment folder on the remote cluster.
            neronet_root (str): the file path to neronet folder.
            cluster_address (str): the address of the cluster.
            cluster_port (int): ssh port number of the cluster.
        """
        tmp_dir = pathlib.Path('/tmp/neronet-tmp')
        # rsync the neronet source files to tmp
        neronet.core.osrun(
            'rsync -az "%s" "%s"' %
            (neronet_root /
             'neronet',
             tmp_dir))
        # rsync bin files to tmp
        neronet.core.osrun(
            'rsync -az "%s" "%s"' %
            (neronet_root / 'bin', tmp_dir))
        # rsync the experiment files to tmp
        neronet.core.osrun(
            'rsync -az "%s/" "%s"' %
            (experiment_folder, tmp_dir))
        # rsync tmp dir contents to the remote node
        neronet.core.osrun(
            'rsync -az -e "ssh -p%s" "%s/" "%s:%s"' %
            (cluster_port,
             tmp_dir,
             cluster_address,
             remote_dir))

    def _get_experiment_results(self, experiment_id, remote_dir, local_dir):
        """Get the experiment results from neromum
        Args:
            experiment_id (str): the experiment ID.
            remote_dir (str): the file path to results folder on the remote
                machine.
            local_dir (str): the file path to results folder on the local
                machine.
        """
        experiment = self.experiments[experiment_id]
        cluster_id = experiment['cluster']
        cluster_port = self.clusters['clusters'][cluster_id]['port']
        cluster_address = self.clusters['clusters'][cluster_id]['ssh_address']
        neronet.core.osrun(
            'rsync -az -e "ssh -p%s" "%s:%s" "%s"'
            % (cluster_port, cluster_address,
                remote_dir, local_dir))

class NeromanCli(neronet.daemon.Cli):
    def __init__(self):
        super().__init__(Neroman())
        self.funcs.update({
            'submit' : self.func_submit,
#            'status' : self.func_status,
#            'experiment' : self.func_experiment,
#            'cluster' : self.func_cluster,
#            'user' : self.func_user
        })

    def func_submit(self):
        foo = {'nam': 13}
        process = subprocess.Popen(['neromum', '--input'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout, serr = process.communicate(pickle.dumps(foo), timeout=5.0)
        print('Output:\n%s' % (sout))
        pass

    def func_experiment(self):
        pass

    def func_cluster(self):
        pass

    def func_specify_user(self, name, email):
        """Update user data."""
        self.daemon.preferences['name'] = name
        self.daemon.preferences['email'] = email
        self.daemon._save_config(self.daemon.preferences_file, self.daemon.preferences)


def main():
    """Create a CLI interface object and process CLI arguments."""
    cli = NeromanCli()
    cli.parse_arguments()
