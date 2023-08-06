# -*- coding: utf-8 -*-
"""This module implements the Command Line Interface of Neroman.
"""

from __future__ import print_function
import os.path
import argparse
import sys

import neronet.neroman
from neronet.core import create_config_template as cfgtemplate
from neronet.core import remove_data
from neronet.config_parser import FormatError

def create_argument_parser():
    """Create and return an argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--addexp',
                        metavar='folder',
                        nargs=1,
                        help='Creates experiments according to the config'
                        'file found in the folder')
    parser.add_argument('--delexp',
                        metavar='experiment_id',
                        nargs=1,
                        help='Deletes the experiment with the given ID')
    parser.add_argument('--copyexp',
                        metavar=('experiment_id', 'duplicated_experiment_id'),
                        nargs=2,
                        help='Creates a duplicate of the experiment')
    parser.add_argument('--plot',
                        metavar='experiment_id',
                        nargs='+',
                        help='Plots the experiment with the given ID or tries'
                        ' to create combined plots of the specified ' 
                        'experiments')
    parser.add_argument('--addnode',
                        metavar=('node_id', 'ssh_address'),
                        nargs=2,
                        help='Specify a new node for computing')
    parser.add_argument('--delnode',
                        metavar='node_id',
                        nargs=1,
                        help='Deletes the node with the given ID')
    parser.add_argument('--submit',
                        metavar=('experiment', 'node'),
                        nargs="+",
                        help='Submits an experiment to be run')
    parser.add_argument('--fetch',
                        action='store_true',
                        help='Fetches results of submitted experiments')
    parser.add_argument('--status',
                        metavar='id',
                        nargs='?',
                        const='all',
                        help='Displays neronet status information')
    parser.add_argument('--clean',
                        action='store_true',
                        help='Removes files created by neroman')
    parser.add_argument('--template',
                        nargs='+',
                        help='Creates a config template file with the \
                        required fields')
    parser.add_argument('--terminate',
                        metavar='experiment_id',
                        nargs=1,
                        help='Terminates the given experiment')
    return parser

def main():
    """Parses the command line arguments and starts Neroman."""
    parser = create_argument_parser()
    args = parser.parse_args()
    if args.clean:
        answer = raw_input('Do you really want to remove all neronet '
                            'configuration files and experiment data? (y/n) ')
        if answer == 'y':
            remove_data()
            print('Removed neronet configuration files and experiment data!')
        else:
            print('Data removal cancelled.')
        return
    nero = neronet.neroman.Neroman()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    if args.addexp:
        experiment_folder = args.addexp[0]
        changed_exps = {}
        try:
            changed_exps = nero.specify_experiments(experiment_folder)
        except (IOError, FormatError) as e:
            print("Failed to specify experiments:")
            print(e)
            return
        print('Experiment(s) successfully defined')
        if changed_exps:
            for experiment in changed_exps.values():
                print('Changes detected in experiment: %s' % experiment.id)
                while True:
                    answer = raw_input('Do you want to overwrite the old' \
                                    + ' version? (y/n)\n')
                    if answer in ['yes', 'ye', 'y']:
                        nero.replace_experiment(experiment)
                        break
                    elif answer in ['no', 'n']: break
    if args.delexp:
        experiment_id = args.delexp[0]
        try:
            print(''.join(nero.delete_experiment(experiment_id)), end="")
        except IOError:
            print('No experiment with ID "%s"' % experiment_id)
    if args.copyexp:
        experiment_id = args.copyexp[0]
        new_experiment_id = args.copyexp[1]
        try:
            print(''.join(nero.duplicate_experiment(experiment_id, \
                        new_experiment_id)), end="") 
        except IOError as e:
            print(str(e))
    if args.plot:
        if len(args.plot) == 1:
            experiment_id = args.plot[0]
            try:
                print(''.join(nero.plot_experiment(experiment_id)), end="")
            except Exception as e:
                print(str(e))
        else:
            experiment_ids = args.plot
            try:
                print(''.join(nero.combined_plot(experiment_ids)), end="")
            except Exception as e:
                print(str(e))
    if args.addnode:
        if len(args.addnode) < 2:
            print("Please specify the required arguments: node ID and ssh address")
            return
        node_id = args.addnode[0]
        ssh_address = args.addnode[1]
        node_type = 'unmanaged'
        try:
            print(''.join(nero.specify_node(node_id, node_type, ssh_address)), end="")
            print('Defined a new node with ID "%s"' % (node_id))
        except Exception as e:
            print(e)
            return
    if args.delnode:
        node_id = args.delnode[0]
        try:
            print(''.join(nero.delete_node(node_id)), end="")
        except KeyError:
            print('No node with ID "%s"' % node_id)
    if args.status:
        try:
            print(''.join(nero.status_gen(args.status)), end="")
        except IOError as e:
            print(e)
    if args.submit:
        experiment_id = args.submit[0]
        try:
            if len(args.submit) > 1:
                node_id = args.submit[1]
                print(''.join(nero.submit(experiment_id, node_id)), end="")
            else:
                print(''.join(nero.submit(experiment_id)), end="")
        except Exception as err:
            print('Submission failed! Error: %s' % (err))
    if args.fetch:
        print(''.join(nero.fetch()), end="")
    if args.template:
        cfgtemplate(*args.template)
    if args.terminate:
        experiment_id = args.terminate[0]
        print(''.join(nero.terminate_experiment(experiment_id)), end="")

def remove_dir(path):
    os.system('rm -r ' + path)

if __name__ == '__main__':
    main()
