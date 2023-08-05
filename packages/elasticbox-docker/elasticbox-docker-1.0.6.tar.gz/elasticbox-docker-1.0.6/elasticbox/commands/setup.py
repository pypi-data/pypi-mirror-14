"""
ElasticBox Confidential
Copyright (c) 2014 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""


from __future__ import absolute_import

from elasticbox.instance import Instance


def initialize_parser(subparsers):
    parser = subparsers.add_parser('setup', help='Setup container box instance')
    parser.add_argument(dest='box_id')

    parser.set_defaults(func=execute_command)


def execute_command(args):
    Instance.initialize(args.box_id)
