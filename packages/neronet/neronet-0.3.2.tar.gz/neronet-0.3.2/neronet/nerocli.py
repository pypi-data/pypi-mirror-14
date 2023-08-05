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
    parser.add_argument('--plot',
                        metavar='experiment_id',
                        nargs=1,
                        help='Plots the experiment with the given ID')
    parser.add_argument('--addnode',
                        metavar=('cluster_id', 'ssh_address'),
                        nargs=argparse.REMAINDER,
                        help='Specify a new cluster for computing')
    parser.add_argument('--delnode',
                        metavar='cluster_id',
                        nargs=1,
                        help='Deletes the cluster with the given ID')
    parser.add_argument('--user',
                        metavar=('name', 'email'),
                        nargs=2,
                        help='Updates user information')
    parser.add_argument('--submit',
                        metavar=('experiment', 'cluster'),
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
                            'configuration files? (y/n) ')
        if answer == 'y':
            remove_data()
            print('Removed neronet configuration files')
        return
    nero = neronet.neroman.Neroman()
    if args.addexp:
        experiment_folder = args.addexp[0]
        changed_exps = {}
        try:
            changed_exps = nero.specify_experiments(experiment_folder)
        except (IOError, FormatError) as e:
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
        except KeyError:
            print('No experiment with ID "%s"' % experiment_id)
    if args.plot:
        experiment_id = args.plot[0]
        try:
            print(''.join(nero.plot_experiment(experiment_id)), end="")
        except KeyError:
            print('No experiment with ID "%s"' % experiment_id)
    if args.addnode:
        if len(args.addnode) < 2:
            print("Please specify the required arguments: cluster ID and ssh address")
            return
        cluster_id = args.addnode[0]
        ssh_address = args.addnode[1]
        cluster_type = 'unmanaged'
        try:
            print(''.join(nero.specify_cluster(cluster_id, cluster_type, ssh_address)), end="")
            print('Defined a new cluster with ID "%s"' % cluster_id)
        except IOError as e:
            print(e)
            return
    if args.delnode:
        cluster_id = args.delnode[0]
        try:
            print(''.join(nero.delete_cluster(cluster_id)), end="")
        except KeyError:
            print('No cluster with ID "%s"' % cluster_id)
    if args.user:
        name = args.user[0]
        email = args.user[1]
        nero.specify_user(name, email)
    if args.status:
        try:
            print(''.join(nero.status_gen(args.status)), end="")
        except IOError as e:
            print(e)
    if args.submit:
        experiment_id = args.submit[0]
        if len(args.submit) > 1:
            cluster_id = args.submit[1]
            print(''.join(nero.submit(experiment_id, cluster_id)), end="")
        else:
            print(''.join(nero.submit(experiment_id)), end="")
    if args.fetch:
        print(''.join(nero.fetch()), end="")
    if args.template:
        cfgtemplate(*args.template)
    if args.terminate:
        experiment_id = args.terminate[0]
        nero.terminate_experiment(experiment_id)

def remove_dir(path):
    os.system('rm -r ' + path)
if __name__ == '__main__':
    main()
