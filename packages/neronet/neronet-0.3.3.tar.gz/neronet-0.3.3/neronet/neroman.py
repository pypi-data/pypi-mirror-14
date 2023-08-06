# -*- coding: utf-8 -*-
"""This module defines Neroman.

To work with Neroman each experiment must have the following attributes
defined in its config:

* experiment_id: The unique identifier for the experiment
* run_command_prefix: The run command of the experiment
* main_code_file: The code file to be run
* destination_folder: Folder that the experiment is run in on the node.
* parameters: The definition of the experiment parameters
* parameters_format: The format of the experiment parameters
* state: A tuple of the experiment state which is set to 'defined' by this
  function and the time changed
* node: The node that the experiment is running on. Set to
  None by this function
* time_created: Sets the current time as the creation time
* time_modified: The time the experiment was last modified. Sets
  this time to the same as the time created
* path: The absolute path to the folder

"""

import os
import time
import datetime
import collections
import pickle
import shutil
import random
import sys

import neronet.config_parser
import neronet.core
import neronet.node
import neronet.experiment

DATABASE_FILENAME = 'default.yaml'
NODES_FILENAME = 'nodes.yaml'

def formatstr(s, length):
    """return the string s so that it is lenght characters long adding spaces or truncating as necessary
    """
    return ("{:<"+str(length)+"}").format(s)[:length]

class Neroman:

    """The part of Neronet that handles user side things.

    Attributes:
        nodes (dict): A dictionary containing the specified nodes
        database (dict): A dictionary containing the specified experiments
    """

    def __init__(self):
        """Initializes Neroman

        Reads the contents of its attributes from yaml files or creates them
        """
        self.config_parser = neronet.config_parser.ConfigParser()
        self.nodes, self.database = \
            self.config_parser.load_configurations(NODES_FILENAME, \
                    DATABASE_FILENAME)

    def specify_node(self, node_id, node_type, ssh_address):
        """Specify nodes so that Neroman is aware of them.

        Writes node name, address and type to the nodes config file

        Args:
            node_id (str): The name of the node, should be unique
            node_type (str): Type of the node. Either slurm or unmanaged
            ssh_address (str): SSH address of the node

        Raises:
            IOError: if the node type isn't unmanaged or slurm

        """
        if not neronet.node.Node.Type.is_member(node_type):
            raise IOError('Neroman: invalid node type "%s"!' % (node_type))
        node = neronet.node.Node(node_id, node_type, ssh_address)
        try:
            node.test_connection()
            yield('Node successfully accessed! Adding it...')
            self.nodes['nodes'][node_id] = node
            self.config_parser.save_nodes(NODES_FILENAME, self.nodes)
        except RuntimeError as e:
            yield('Error: %s' % (e))

    def delete_node(self, node_id):
        """Deletes the node with the given node ID

        Parameters:
            node_id (str): ID of the node to be deleted
        Raises:
            KeyError: if the node with the given ID doesn't exist
        """
        if node_id in self.nodes['nodes']:
            del self.nodes['nodes'][node_id]
            self.config_parser.save_nodes(NODES_FILENAME, self.nodes)
            yield('Node "%s" deleted.' % (node_id))

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
        if not os.path.isdir(folder):
            folder = os.path.dirname(folder)
        experiments = self.config_parser.parse_experiments(folder)
        err = []
        #Look for changes in the relevant fields and add them to changed_exps.
        #FIXME: Change this functionality so that the comaprison is done in the
        #experiment side and not on neroman
        changed_exps = {}
        relevant_fields = neronet.experiment.MANDATORY_FIELDS | \
                        neronet.experiment.OPTIONAL_FIELDS | set('path')
        for experiment in experiments:
            if experiment.id in self.database:
                for key in experiment._fields:
                    if key in relevant_fields and self.database[experiment.id].__getattr__(key) \
                                                    != experiment.__getattr__(key):
                        changed_exps[experiment.id] = experiment
                        break
                err.append("Experiment named %s already in the database" \
                            % experiment.id)
            else: self.database[experiment.id] = experiment
        self.config_parser.save_database(DATABASE_FILENAME, \
                                    self.database)
        if err: raise IOError('\n'.join(err))
        return changed_exps

    def replace_experiment(self, new_experiment):
        """Replaces an experiment in the database with a new,
        updated instance of it.

        Parameters:
            new_experiment (neronet.experiment.Experiment): the experiment object
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
        if experiment_id not in self.database:
            raise IOError("Neroman: %s is not in database" % experiment_id)
        if self.database[experiment_id]._fields['node_id']:
            self.terminate_experiment(experiment_id)
        self.database.pop(experiment_id)
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)
        yield "Experiment '%s' successfully deleted\n" % experiment_id

    def duplicate_experiment(self, experiment_id, new_experiment_id):
        if experiment_id not in self.database:
            raise IOError("Neronet: %s is not in database" % experiment_id) 
        if new_experiment_id in self.database:
            raise IOError("Neronet: %s already in database" \
                            % new_experiment_id)
        experiment = self.database[experiment_id]
        duplicated_experiment = neronet.experiment.duplicate_experiment( \
                                            experiment, new_experiment_id)
        self.database[new_experiment_id] = duplicated_experiment
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)
        yield "Copied experiment %s into %s\n" % (experiment_id, \
                                                new_experiment_id)

    def plot_experiment(self, experiment_id):
        """ Plots the experiemnt according to plotting specifications
        """
        if experiment_id not in self.database:
            raise IOError("Neronet: %s is not in database" % experiment_id)
        experiment = self.database[experiment_id]
        experiment.plot_outputs()
        yield "Plotted experiment %s\n" % experiment_id
    
    def combined_plot(self, experiment_ids):
        """ Tries to 
        """
        experiments = []
        plots = None
        first = True
        feedbacks = {}
        for experiment_id in experiment_ids:
            if experiment_id not in self.database:
                raise IOError("Neronet: %s is not in database" \
                                % experiment_id)
            experiment = self.database[experiment_id]
            if first:
                if experiment.plot:
                    plots = experiment.plot
            else:
                if experiment.plot:
                    for plot in plots:
                        if plot not in experiment.plot or \
                                plots[plot] != experiment.plot[plot]:
                            del plots[plot]
                        
            experiments.append(experiment)
            first = False
        if not plots:
            raise IOError("Neroman: no combinable plots")

        for plot in plots:
            feedbacks[plot] = None
        for experiment in experiments[:-1]:
            for plot in plots:
                feedback = feedbacks[plot]
                feedbacks[plot] = experiment.plotter(plot, feedback, False)
        for plot in plots:
            feedback = feedbacks[plot]
            experiment = experiments[-1]
            saved_name = '_'.join(experiment_ids + [plot])
            experiment.plotter(plot, feedback, True, saved_name)
        yield "Successfully plotted experiments\n"

    def terminate_experiment(self, experiment_id):
        if experiment_id in self.database:            
            node_id = self.database[experiment_id]._fields['node_id']
            if node_id:
                node = self.nodes['nodes'][node_id]
                try:
                    node.terminate_exp(experiment_id)
                    yield 'Termination message successfully sent to neromum'
                except RuntimeError:
                    yield 'Failed to terminate the given experiment. This could be a result of the experiment already being terminated or finished.'                
            else:
                yield '"%s" hasn\'t been submitted to node or has already finished running' % (experiment_id)
        else:
            yield '"%s", No such experiment' % (experiment_id) 

    def status_gen(self, arg):
        """Creates a generator that generates the polled status

        Yields:
            str: A line of neroman status
        """
        if arg != 'all':
            if arg == 'nodes':
                if not self.nodes['nodes']:
                    yield 'No nodes defined\n'
                else:
                    yield '{0:<11} {1:<11} {2:<15} {3:<6} {4:<4} {5:<4}\n'.format('Name','Type','Address','Load', '%Mem', '%Dsk')
                    for node in self.nodes['nodes'].values():
                        resources = node.gather_resource_info()
                        yield '{0:<11} {1:<11} {2:<15} {3:<6} {4:<4.3} {5:<4}\n'.format(node.cid, node.ctype, node.ssh_address[:15], resources['avgload'], 100.0*int(resources['usedmem'])/int(resources['totalmem']), resources['percentagediskspace'])

                raise StopIteration
            elif arg in self.database:
                experiment = self.database[arg]
                for line in experiment.as_gen():
                    yield line
                raise StopIteration
            elif arg in self.nodes['nodes']:
                node = self.nodes['nodes'][arg]
                yield "\n%s\n" % node.cid
                yield "===========\n"
                yield "SSH Address: %s\n" % node.ssh_address
                yield "Type: %s\n" % node.ctype
                yield "Experiments in node:\n"
                noexperiments = True
                for exp in self.database:
                    if self.database[exp].node_id == node.cid:
                        noexperiments = False
                        yield "  Experiment id: %s, Status: %s\n" \
                                % (exp, self.database[exp].state)
                if noexperiments: yield "  No experiments in node.\n"
                resources = node.gather_resource_info()
                yield "Average load 15min: %s\n" % resources['avgload']
                yield "Memory usage in MiB: %s out of %s total.(%.2f%%)\n" % (resources['usedmem'], resources['totalmem'], 100.0*int(resources['usedmem'])/int(resources['totalmem']))
                yield "Disk space in MiB: %s out of %s total. (%s)\n" % (resources['useddiskspace'], resources['totaldiskspace'], resources['percentagediskspace'])
                raise StopIteration
            else:
                raise IOError('Neroman: no experiment or node named "%s"!'\
                                % (arg))
        #yield "\n"
        yield "=> Nodes =>\n"
        if not self.nodes['nodes']:
            yield 'No nodes defined\n'
        else:
            # Sort in descending order by ID
            for node in sorted(self.nodes['nodes'].itervalues(), key=lambda n: n.cid):
                yield '- %s (%s)\n' % (node.cid, node.ssh_address)
        if self.nodes['groups']:
            yield "Node groups:\n"
            groups = self.nodes['groups']
            for group_id, group_nodes in groups.iteritems():
                yield '- %s: %s\n' % (group_id, ', '.join(node for node in group_nodes))
        if 'default_node' in self.nodes and self.nodes['default_node']:
            yield "Default Node: %s\n" % self.nodes['default_node']
        yield "\n=> Experiments =>\n"
        if not len(self.database):
            yield "No experiments defined\n"
        else:
            experiments_by_state = self._experiments_by_state(self.database)
            current = ""
            # Sort in descending order by state and then by ID
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

    def submit(self, exp_id, node_id=""):
        """Submit an experiment to a node using SSH.

        Args:
            exp_id (str): the ID of the experiment.
            node_id (str): the ID of the node.
        """
        # Determine the node
        if not node_id:
            node_id = self.nodes['default_node']
            if node_id == "":
                raise AttributeError('No default node defined')
        #if node_id in self.nodes['groups']:
           # node_id = random.choice(self.nodes['groups'][node_id])
        if node_id in self.nodes['groups']:
            avg_load = 999.0
            cl_id = None
            for cl in self.nodes['groups'][node_id]:
                try:
                    node = self.nodes['nodes'][cl]
                    node.update_average_load(node.sshrun('uptime').out[-5:-1])
                except RuntimeError:
                    node.update_average_load("undefined")
                    continue
                self.config_parser.save_nodes(NODES_FILENAME, self.nodes)
                if float(node.average_load) < avg_load:
                    avg_load = node.average_load
                    cl_id = cl
                else:
                    continue
            if cl_id == None:
                raise AttributeError('No valid nodes in the node group')
            else:
                node_id = cl_id
        elif node_id not in self.nodes['nodes']:
            raise AttributeError('The given node ID "%s" is not valid!' %
                    (node_id))
        node = self.nodes["nodes"][node_id]
        # Load the experiment
        if exp_id not in self.database:
            raise AttributeError('The given experiment ID "%s" is not valid!' %
                    (exp_id))
        exp = self.database[exp_id]

        if exp.node_id != None:
            raise Exception('Experiment already submitted to "%s"! '
                    % (exp.node_id)  +
             'If you wish to re-submit the same experiment, you need to wait for your experiment to finish or terminate it with "nerocli --terminate ID" where ID is the id of your experiment.')
        # Update experiment info
        exp.node_id = node_id
        exp.update_state(neronet.experiment.Experiment.State.submitted)
        self.config_parser.save_nodes(NODES_FILENAME, self.nodes)
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
        # Finally, serialize the node object into the tmp folder
        neronet.core.write_file(os.path.join(local_tmp_dir, 'node.pickle'),
                pickle.dumps(node))
        # Transfer the files to the remote server
        try:
            neronet.core.osrun('rsync -az -e "ssh" "%s/" "%s:%s"' %
                (local_tmp_dir, node.ssh_address, remote_dir))
            # Start the Neromum daemon
            node.start_neromum()
            yield("Experiment " + exp_id + " successfully submitted to " + node_id + "\n")
        finally:
            # Remove the temporary directory
            shutil.rmtree(local_tmp_dir)
        # Update the experiment database
        self.config_parser.save_database(DATABASE_FILENAME, self.database)

    def fetch(self):
        """Fetch results of submitted experiments."""
        experiments_to_check = set()
        nodes_to_fetch = set()
        # Find out the experiments that have been submitted to some node
        # and the associated nodes
        for exp in self.database.values():
            if exp.node_id != None:
                experiments_to_check.add(exp)
                nodes_to_fetch.add(exp.node_id)
        # Define source and destination directories
        remote_dir = os.path.join(neronet.core.USER_DATA_DIR,
                'experiments')
        local_dir = os.path.join(neronet.core.USER_DATA_DIR_ABS,
                'results')
        # Fetch the changes from the nodes
        for node_id in nodes_to_fetch:
            yield('Fetching changes from node "%s"...' % (node_id))
            # Load node details
            node = self.nodes['nodes'][node_id]
            # Fetch the files from the remote server
            try:
                neronet.core.osrun('rsync -az -e "ssh" "%s:%s/" "%s"' %
                    (node.ssh_address, remote_dir, local_dir))
            except RuntimeError:
                yield('Err: Failed to fetch experiment results from node "%s".' % (node.cid))
            # Clean the node
        plot_errors = []
        #Update Neroman database contents from the fetched pickles
        for exp in experiments_to_check:
            # Update the experiments
            yield('Updating experiment "%s"...\n' % (exp.id))
            exp_file = os.path.join(local_dir, exp.id, 'exp.pickle')
            if not os.path.exists(exp_file):
                yield('ERR: Experiment pickle missing!')
                exp.update_state(neronet.experiment.Experiment.State.lost)
                continue
            exp = self.database[exp.id] = pickle.loads(
                    neronet.core.read_file(exp_file))
            
            if exp.state in (neronet.experiment.Experiment.State.finished,
                        neronet.experiment.Experiment.State.lost, 
                        neronet.experiment.Experiment.State.terminated):
                exp.node_id = None
                if exp.state == neronet.experiment.Experiment.State.finished:
                    results_dir = os.path.join(exp.path, 'results')
                    if not os.path.exists(results_dir):
                        os.mkdir(results_dir)
                    result_destination = os.path.join(results_dir, '%s-%s'
                            % (exp.id, time.strftime('%Y-%m-%d-%H-%M-%S',
                            time.localtime())))
                    shutil.move(os.path.join(local_dir, exp.id), result_destination) 
                    exp.run_results.append(result_destination)
                    try:
                        if exp.plot:
                            exp.plot_outputs()
                    except Exception as e:
                        yield str(e)
        self.config_parser.save_database(DATABASE_FILENAME, self.database)
        #Try to clean finished/terminated/lost experiments from remote nodes
        for node_id in nodes_to_fetch:
            node = self.nodes['nodes'][node_id]
            node.start_neromum()
            exceptions = [exp.id for exp in self.database.values() if exp.state
                            in (neronet.experiment.Experiment.State.submitted,
                            neronet.experiment.Experiment.State.submitted_to_kid,
                            neronet.experiment.Experiment.State.running) and exp.node_id == node_id]
            try:
                node.clean_experiments(exceptions)
            except RuntimeError:
                yield('Note: Failed to clean the experiments at the node.')


    #def tail_log(self, exp_id=None):
    #    """List latest log file lines of submitted experiments."""
    #    for exp in self.database.values():
    #        if exp.node_id != None:
