#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Tool to manage YAML CMDB.
    Support ivan.bogomazov@gmail.com
    Minsk 2017


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    EXAMPLES:

    $ ./tools/parser.py -k common.bake.base_ami ../cmdb/stacks/dev1.yml
    ami-a8d2d7ce
    ...

    $ ./tools/parser.py -a jump ../cmdb/stacks/dev1.yml
    apps:
        ansible_branch: master
        app_branch: master
    common:
        bake:
            ami_size: 20
            ...
        stack:
            domain_zone: example.com
            fqdn: dev1.example.com
            ldap_server: ldap.dev1.example.com
            name: dev1
            ...
            region: us-east-2
"""

from __future__ import print_function

import os
import sys

import argparse
import json
import yaml


def parse_arguments():
    """Argument parsing

    :return: args namespace
    :rtype: namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'cmdb_file',
        type=str,
        help='Path to cmdb settings file',
    )

    parser.add_argument(
        '-a',
        '--app',
        dest='app',
        type=str,
        help='Application name',
    )

    parser.add_argument(
        '-k',
        '--key',
        dest='key',
        type=str,
        help='Path to cmdb section',
    )

    parser.add_argument(
        '-t',
        '--table-versions',
        dest='table',
        action="store_true",
        help='Print applications versions',
    )


    parser.add_argument(
        '-f',
        '--format',
        dest='dumper',
        choices=[
            'yaml',
            'json',
        ],
        default='yaml',
        help='Output format. Default json',
    )

    return parser.parse_args()


def load_yaml(path_to_yaml):
    """JSON parser

    :param path_to_yaml: path to yaml file
    :type path_to_json: str

    :return: yaml data
    :rtype: dict
    """
    try:
        with open(path_to_yaml, 'r') as _fp:
            return yaml.load(_fp)

    except ValueError as error:
        sys.stderr.write("Bad format {0}: {1}".format(
            path_to_yaml,
            error
        ))
        exit(100)

    except OSError as error:
        sys.stderr.write("Bad file {0}: {1}".format(
            path_to_yaml,
            error
        ))
        exit(101)

    except yaml.parser.ParserError as error:
        sys.stderr.write("Broken yaml {0}: {1}".format(
            path_to_yaml,
            error
        ))
        exit(102)

    except yaml.composer.ComposerError as error:
        sys.stderr.write("Broken anchor {0}: {1}".format(
            path_to_yaml,
            error
        ))
        exit(103)


def get_specified_key(data, key):
    """Get specified key from dataset.
    For key apps.v2api.app_branch returns:
    'tags/2.0.0'

    :param data: configuration dataset
    :type data: dict

    :return: value of specified key
    :rtype: dict or list or str
    """
    path = key.split('.')

    for key in path:
        sub_data = data.get(key)
        data = sub_data

    return data


def get_app_section(data, app):
    """Return provided application dataset and common data
    For v2api returns:
    {'apps': {'v2api': sub_data}, 'common': {}}

    :param data: configuration dataset
    :type data: dict

    :param app: application name
    :type app: str

    :return: configuration dataset
    :rtype: data: dict
    """
    return {
        'common': data.get('common', {}),
        'apps': {
            app: data.get('apps', {}).get(app, {})
        },
    }


def get_apps(data):
    """Return configuration dataset for all applications

    :param data: configuration dataset
    :type data: dict

    :return: configuration dataset
    :rtype: data: dict
    """
    data.pop('mapping')
    return data


def print_settings(data, dumper):
    """Printing resulted dataset

    :param data: configuration dataset
    :type data: dict

    :return: printing dataset in format to stdout
    :rtype: None

    """
    if dumper == "json":
        print(
            json.dumps(
                data,
                indent=4
            )
        )
    else:
        noalias_dumper = yaml.dumper.SafeDumper
        noalias_dumper.ignore_aliases = lambda self, data: True
        print(
            yaml.dump(
                data,
                indent=4,
                default_flow_style=False,
                Dumper=noalias_dumper,
            )
        )


def main():
    """Main"""
    args = parse_arguments()
    data = load_yaml(args.cmdb_file)

    if args.key:
        print_settings(
            get_specified_key(
                data,
                args.key
            ),
            args.dumper
        )
    elif args.app:
        print_settings(
            get_app_section(
                data,
                args.app
            ),
            args.dumper
        )
    elif args.table:
        # vpergament tool for application versions
        row_format = '{:>15}{:>15}'
        print('\n Version table for', os.path.basename(args.cmdb_file), '\n')
        for app_name, app_data in data.get('apps', {}).iteritems():
            print(row_format.format(
                app_name,
                app_data.get('app_branch', 'None').replace('tags/', '')
            ))
    else:
        print_settings(
            get_apps(data),
            args.dumper
        )

if __name__ == '__main__':
    main()
