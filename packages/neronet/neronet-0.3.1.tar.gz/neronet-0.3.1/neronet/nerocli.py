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
    parser.add_argument('--experiment',
                        metavar='folder',
                        nargs=1,
                        help='Creates experiments according to the config'
                        'file found in the folder')
    parser.add_argument('--delete',
                        metavar='experiment_id',
                        nargs=1,
                        help='Deletes the experiment with the given ID')
    parser.add_argument('--plot',
                        metavar='experiment_id',
                        nargs=1,
                        help='Plots the experiment with the given ID')
    parser.add_argument('--cluster',
                        metavar=('cluster_id', 'type', 'ssh_address'),
                        nargs=argparse.REMAINDER,
                        help='Specify a new cluster for computing')
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
    if args.experiment:
        experiment_folder = args.experiment[0]
        changed_exps = {}
        try:
            changed_exps = nero.specify_experiments(experiment_folder)
        except (IOError, FormatError) as e:
            print(e)
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
    if args.delete:
        experiment_id = args.delete[0]
        try:
            nero.delete_experiment(experiment_id)
        except KeyError:
            print("No experiment named %s" % experiment_id)
    if args.plot:
        experiment_id = args.plot[0]
        try:
            nero.plot_experiment(experiment_id)
        except KeyError:
            print("No experiment named %s" % experiment_id)
    if args.cluster:
        if len(args.cluster) < 3:
            print("Please specify the required arguments: cluster Id, cluster type and ssh address")
            return
        cluster_id = args.cluster[0]
        cluster_type = args.cluster[1]
        ssh_address = args.cluster[2]
        try:
            nero.specify_cluster(cluster_id, cluster_type, ssh_address)
            print("Defined a new cluster named " + cluster_id)
        except IOError as e:
            print(e)
            return
    if args.user:
        name = args.user[0]
        email = args.user[1]
        nero.specify_user(name, email)
    if args.status:
        try:
            status_gen = nero.status_gen(args.status)
            print(''.join(status_gen), end="")
        except IOError as e:
            print(e)
    if args.submit:
        experiment_id = args.submit[0]
        if len(args.submit) > 1:
            cluster_id = args.submit[1]
            nero.submit(experiment_id, cluster_id)
        else:
            nero.submit(experiment_id)
    if args.fetch:
        nero.fetch()
    if args.template:
        cfgtemplate(*args.template)
    if args.terminate:
        experiment_id = args.terminate[0]
        nero.terminate_experiment(experiment_id)

def remove_dir(path):
    os.system('rm -r ' + path)
if __name__ == '__main__':
    main()
