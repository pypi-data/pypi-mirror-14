#! /usr/bin/env python

import sys
import argparse
import pkg_resources
from common.cluster_config import PRESTO_CONTAINERS, CONTAINER_HADOOP
from common import cluster
import presto_build
import hadoop_build
import status


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_version_sub_parser(subparsers)
    add_status_sub_parser(subparsers)
    add_hadoop_sub_parser(subparsers)
    add_presto_sub_parser(subparsers)
    return parser


def add_status_sub_parser(subparsers):
    add_command_parser(subparsers, 'status', 'Containers & Services status', status.run)


def add_version_sub_parser(subparsers):
    add_command_parser(subparsers, 'version', 'Display version', display_version)


def add_hadoop_sub_parser(subparsers):
    hadoop_parser = subparsers.add_parser('hadoop', help='Hadoop container management')
    hadoop_subparsers = hadoop_parser.add_subparsers()
    add_command_parser(hadoop_subparsers, 'start', 'Start local hadoop', hadoop_start)
    add_command_parser(hadoop_subparsers, 'stop', 'Stop local hadoop', hadoop_stop)
    add_command_parser(hadoop_subparsers, 'clean', 'Clean hadoop', hadoop_clean)
    add_command_parser(hadoop_subparsers, 'build-image', 'Build hadoop image', hadoop_build.run)


def add_presto_sub_parser(subparsers):
    presto_parser = subparsers.add_parser('presto', help='Presto containers management')
    presto_subparsers = presto_parser.add_subparsers()
    add_command_parser(presto_subparsers, 'start', 'Start presto cluster', presto_start)
    add_command_parser(presto_subparsers, 'stop', 'Stop presto cluster', presto_stop)
    add_command_parser(presto_subparsers, 'clean', 'Clean presto cluster', presto_clean)
    add_command_parser(presto_subparsers, 'build-image', 'Build presto image', presto_build.run)


def add_command_parser(subparsers, command, command_help, target=None):
    parser = subparsers.add_parser(command, help=command_help, add_help=False)
    parser.set_defaults(command=command, target=target)
    return parser


def presto_start(args):
    if not cluster.is_running(CONTAINER_HADOOP.container_name):
        raise Exception("You need to start hadoop first")
    for container in PRESTO_CONTAINERS.values():
        cluster.start(container.container_name)


def presto_stop(args):
    for container in PRESTO_CONTAINERS.values():
        cluster.stop(container.container_name)


def presto_clean(args):
    for container in PRESTO_CONTAINERS.values():
        cluster.clean(container.container_name)


def hadoop_start(args):
    cluster.start(CONTAINER_HADOOP.container_name)


def hadoop_stop(args):
    cluster.stop(CONTAINER_HADOOP.container_name)


def hadoop_clean(args):
    cluster.clean(CONTAINER_HADOOP.container_name)


def display_version(args):
    version = pkg_resources.get_distribution("presto-docker-devenv").version
    print "Version of Presto docker developer environment: %s" % version


def main():
    parser = create_parser()
    arguments, extra = parser.parse_known_args(sys.argv[1:])
    exit(arguments.target(extra))
