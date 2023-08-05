# -*- coding: utf-8 -*-
from __future__ import print_function
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

"""

import os
import time
import datetime
import os.path
import collections
import pickle
import shutil
import random
import sys

import neronet.core
import neronet.config_parser

DATABASE_FILENAME = 'default.yaml'
PREFERENCES_FILENAME = 'preferences.yaml'
CLUSTERS_FILENAME = 'clusters.yaml'

class Neroman:

    """The part of Neronet that handles user side things.

    Attributes:
        clusters (Dict): A dictionary containing the specified clusters
        database (Dict): A dictionary containing the specified experiments
        preferences (Dict): A dictionary containing the preferences
    """

    def __init__(self):
        """Initializes Neroman

        Reads the contents of its attributes from yaml files or creates them
        """
        self.config_parser = neronet.config_parser.ConfigParser()
        self.clusters, self.preferences, self.database = \
            self.config_parser.load_configurations(CLUSTERS_FILENAME, \
                            PREFERENCES_FILENAME, DATABASE_FILENAME)

    def clean(self):
        """Removes all neronet related data"""
        self.config_parser.remove_data()

    def specify_cluster(self, cluster_id, cluster_type, ssh_address):
        """Specify clusters so that Neroman is aware of them.

        Writes cluster name, address and type to the clusters config file

        Args:
            cluster_id (str): The name of the cluster, should be unique
            cluster_type (str): Type of the cluster. Either slurm or unmanaged
            ssh_address (str): SSH address of the cluster

        Raises:
            IOError: if the cluster type isn't unmanaged or slurm

        """
        if not neronet.core.Cluster.Type.is_member(cluster_type):
            raise IOError('Invalid cluster type "%s"!' % (cluster_type))
        cluster = neronet.core.Cluster(cluster_id, cluster_type, ssh_address)
        try:
            cluster.test_connection()
            print('The cluster seems to be online!')
        except RuntimeError as e:
            print('Warning: %s' % (e))
        self.clusters['clusters'][cluster_id] = cluster
        self.config_parser.save_clusters(CLUSTERS_FILENAME, self.clusters)

    def specify_experiments(self, folder):
        """Specify experiments so that Neroman is aware of them.

        Reads the contents of the experiment from a config file inside the
        specified folder.

        Args:
            folder (str): The path of the folder that includes
                the experiment that's being specified.

        Raises:
            IOError: If the folder doesn't exists or the config file
                doesn't exists
            FormatError: If the config file is badly formated

        Returns:
            changed_exps: A dictionary of changed experiments. 
                This is then later used to prompt the user if they
                want to replace the old experiment(s) with the new one(s).
        """


        experiments = self.config_parser.parse_experiments(folder)
        err = []
        #Look for changes in the relevant fields and add them to changed_exps.
        changed_exps = {}
        relevant_fields = neronet.core.MANDATORY_FIELDS | neronet.core.OPTIONAL_FIELDS | set('path')
        for experiment in experiments:
            if experiment.id in self.database:
                for key in experiment._fields:
                    if key in relevant_fields and self.database[experiment.id].__getattr__(key) \
                                                    != experiment.__getattr__(key):
                        #(debug)print('Key: %s, Old: %s, New: %s' % (key, \
                        #        self.database[experiment.id].__getattr__(key), 
                        #        experiment.__getattr__(key)))
                        changed_exps[experiment.id] = experiment
                        break
                err.append("Experiment named %s already in the database" \
                            % experiment.id)
            else: self.database[experiment.id] = experiment
        self.config_parser.save_database(DATABASE_FILENAME, \
                                    self.database)
        if err: print('\n'.join(err), file=sys.stderr)
        return changed_exps
    
    def specify_user(self, name, email, default_cluster = ""):
        """Update user data"""
        self.preferences['name'] = name
        self.preferences['email'] = email
        self.preferences['default_cluster'] = default_cluster
        self.config_parser.save_preferences(PREFERENCES_FILENAME, \
                                            self.preferences)

    def replace_experiment(self, new_experiment):
        """Replaces an experiment in the database with a new,
        updated instance of it.

        Parameters:
            new_experiment (neronet.core.Experiment): the experiment object
                    to be put in the database in place of the old one.
        """
        self.database[new_experiment.id] = new_experiment
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)

    def delete_experiment(self, experiment_id):
        """Deletes the experiment with the given experiment id

        Parameters:
            experiment_id (str): id of the experiment to be deleted
        Raises:
            KeyError: if the experiment with the given id doesn't exist
        """
        self.database.pop(experiment_id)
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)

    def plot_experiment(self, experiment_id):
        experiment = self.database[experiment_id]
        experiment.plot_output()

    def status_gen(self, arg):
        """Creates a generator that generates the polled status

        Yields:
            str: A line of neroman status
        """
        if arg != 'all':
            if arg in self.database:
                experiment = self.database[arg]
                for line in experiment.as_gen():
                    yield line
                raise StopIteration
            elif arg in self.clusters['clusters']:
                cluster = self.clusters['clusters'][arg]
                for ln in cluster.yield_status():
                    yield ln
                raise StopIteration
            else:
                raise IOError('No experiment or cluster named "%s"!' % (arg))
        yield "================Neroman=================\n"
        yield "\n"
        yield "================User====================\n"
        yield "Name: %s\n" % self.preferences['name']
        yield "Email: %s\n" % self.preferences['email']
        if self.preferences['default_cluster']:
            yield "Default Cluster: %s\n" % self.preferences['default_cluster']
        yield "\n"
        yield "================Clusters================\n"
        yield 'Clusters:\n'
        if not self.clusters['clusters']:
            yield 'No clusters defined\n'
        else:
            for cid, cluster in self.clusters['clusters'].iteritems():
                yield '- %s\n' % (cluster)
            if self.clusters['groups']:
                yield "Cluster groups:\n"
                groups = self.clusters['groups']
                for group_id, group_clusters in groups.iteritems():
                    yield '- %s: %s\n' % (group_id, ', '.join(cluster for cluster in group_clusters))
        yield "\n"
        yield "================Experiments=============\n"
        if not len(self.database):
            yield "No experiments defined\n"
        else:
            experiments_by_state = self._experiments_by_state(self.database)
            current = ""
            for state, experiments in sorted(experiments_by_state.iteritems()):
                yield "%s:\n" % state.capitalize()
                for experiment in sorted(experiments, key=lambda e: e.id):
                    exp_warnings_exist = experiment.has_warnings()
                    yield str("- %s" % experiment.id) + ' ' + exp_warnings_exist + '\n'

    def _experiments_by_state(self, experiments, state=None):
        """Partitions the experiments in the database by state"""
        experiments_by_state = collections.defaultdict(list)
        for experiment in experiments.values():
            if not state or experiment.state == state:
                experiments_by_state[experiment.state].append(experiment)
        return experiments_by_state

    def submit(self, exp_id, cluster_id=""):
        """Submit an experiment to a cluster using SSH.

        Args:
            exp_id (str): the ID of the experiment.
            cluster_id (str): the ID of the cluster.
        """
        # Determine the cluster
        if not cluster_id:
            cluster_id = self.preferences['default_cluster']
        if cluster_id in self.clusters['groups']:
            cluster_id = random.choice(self.clusters['groups'][cluster_id])
        if cluster_id not in self.clusters['clusters']:
            raise AttributeError('The given cluster ID "%s" is not valid!' %
                    (cluster_id))
        cluster = self.clusters["clusters"][cluster_id]
        # Load the experiment
        exp = self.database[exp_id]
        #TODO: offer to cancel the current experiment submission
        #if exp.cluster_id != None: # (Commented for debugging)
        #    raise Exception('Experiment already submitted to "%s"!'
        #            % (exp.cluster_id))
        # Update experiment info
        exp.cluster_id = cluster_id
        exp.update_state(neronet.core.Experiment.State.submitted)
        # Define local path, where experiment currently exists
        local_exp_path = exp.path
        # Define the remote path into which the files will be transferred to,
        # assuming it will be under the user's home directory
        remote_dir = neronet.core.USER_DATA_DIR
        # Define a temporary folder to contain all the required files
        local_tmp_dir = '/tmp/.neronet-%s' % (exp.id)
        # Define a folder for the files required by the experiment
        local_tmp_exp_dir = os.path.join(local_tmp_dir, 'experiments', exp.id)
        # Create the local temporary directories
        os.makedirs(local_tmp_exp_dir)
        # Define paths to required Neronet files
        neronet_root_dir = os.path.dirname(os.path.abspath(__file__))
        # Add Neronet source code files and executables to the temporary dir
        neronet.core.osrun('rsync -az "%s" "%s"' %
                (neronet_root_dir, local_tmp_dir))
        # Add the experiment files
        for file_path in exp.required_files + [exp.main_code_file]:
            neronet.core.osrun('cp -p "%s" "%s"' %
                (os.path.join(local_exp_path, file_path), local_tmp_exp_dir))
        # Serialize the experiment object into the experiment folder
        neronet.core.write_file(os.path.join(local_tmp_exp_dir, 'exp.pickle'),
                pickle.dumps(exp))
        # Finally, serialize the cluster object into the tmp folder
        neronet.core.write_file(os.path.join(local_tmp_dir, 'cluster.pickle'),
                pickle.dumps(cluster))
        # Transfer the files to the remote server
        try:
            neronet.core.osrun('rsync -az -e "ssh" "%s/" "%s:%s"' %
                (local_tmp_dir, cluster.ssh_address, remote_dir))
            # Start the Neromum daemon
            cluster.start_neromum()
            print("Experiment " + exp_id + " successfully submitted to " + cluster_id)
        finally:
            # Remove the temporary directory
            shutil.rmtree(local_tmp_dir)
        # Update the experiment database
        self.config_parser.save_database(DATABASE_FILENAME, self.database)

    def fetch(self):
        """Fetch results of submitted experiments."""
        experiments_to_check = set()
        clusters_to_fetch = set()
        # Find out the experiments that have been submitted to some cluster
        # and the associated clusters
        for exp in self.database.values():
            if exp.cluster_id != None:
                experiments_to_check.add(exp)
                clusters_to_fetch.add(exp.cluster_id)
        # Define source and destination directories
        remote_dir = os.path.join(neronet.core.USER_DATA_DIR,
                'experiments')
        local_dir = os.path.join(neronet.core.USER_DATA_DIR_ABS,
                'results')
        # Fetch the changes from the clusters
        for cluster_id in clusters_to_fetch:
            print('Fetching changes from cluster "%s"...' % (cluster_id))
            # Load cluster details
            cluster = self.clusters['clusters'][cluster_id]
            # Fetch the files from the remote server
            try:
                neronet.core.osrun('rsync -az -e "ssh" "%s:%s/" "%s"' %
                    (cluster.ssh_address, remote_dir, local_dir))
            except RuntimeError:
                print('Err: Failed to fetch experiment results from cluster "%s".' % (cluster.cid))
            # Clean the cluster
            exceptions = [exp.id for exp in experiments_to_check if exp.state
                    in (neronet.core.Experiment.State.submitted,
                    neronet.core.Experiment.State.submitted_to_kid,
                    neronet.core.Experiment.State.running)]
            try:
                cluster.clean_experiments(exceptions)
            except RuntimeError:
                print('Note: Failed to clean the experiments at the cluster.')
        # Update the experiments
        for exp in experiments_to_check:
            print('Updating experiment "%s"...' % (exp.id))
            exp_file = os.path.join(local_dir, exp.id, 'exp.pickle')
            if not os.path.exists(exp_file):
                print('ERR: Experiment pickle missing!')
                exp.update_state(neronet.core.Experiment.State.lost)
                continue
            exp = self.database[exp.id] = pickle.loads(
                    neronet.core.read_file(exp_file))
            if exp.state in (neronet.core.Experiment.State.finished,
                        neronet.core.Experiment.State.lost):
                exp.cluster_id = None
                #TODO: Do output processing
                if exp.state == neronet.core.Experiment.State.finished:
                    results_dir = os.path.join(exp.path, 'results')
                    if not os.path.exists(results_dir):
                        os.mkdir(results_dir)
                    shutil.move(os.path.join(local_dir, exp.id), \
                                os.path.join(results_dir, exp.id))
                    print(exp.output_processor)
                    if exp.output_processor:
                        exp.plot_output()
        self.config_parser.save_database(DATABASE_FILENAME, self.database)

    #def tail_log(self, exp_id=None):
    #    """List latest log file lines of submitted experiments."""
    #    for exp in self.database.values():
    #        if exp.cluster_id != None:
