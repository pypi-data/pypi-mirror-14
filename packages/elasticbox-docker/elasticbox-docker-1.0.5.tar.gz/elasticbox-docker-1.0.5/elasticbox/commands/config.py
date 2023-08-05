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

import os
import sys

from elasticbox.instance import Instance
from elasticbox.session import AuthenticatedSession


def initialize_parser(subparsers):
    parser = subparsers.add_parser('config', help='Sets the value of a variable')
    parser.add_argument('--instance-id', required=False, default=os.getenv('INSTANCE_ID', 'local'), dest='instance_id')
    parser.add_argument('--scope', required=False, default=os.getenv('ELASTICBOX_SCOPE', None), dest='scope')
    parser.add_argument('--input', '-i', required=False, dest='input', help='Template file to process')
    parser.add_argument('--output', '-o', required=False, dest='output', help='Output file')
    parser.set_defaults(func=execute_command)


def execute_command(args):
    if args.token:
        session = AuthenticatedSession(args)
    else:
        session = None

    instance = Instance(args.instance_id, session)

    if args.input is not None:
        with open(args.input, 'r') as template:
            contents = template.read().decode('utf-8')
    else:
        contents = sys.stdin.read().decode('utf-8')

    if args.output is not None:
        with open(args.output, 'w') as output:
            print >> output, instance.config(contents, args.scope)
    else:
        print >> sys.stdout, instance.config(contents, args.scope)
