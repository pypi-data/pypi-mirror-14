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
import signal
import sys
import time

from elasticbox.instance import Instance
from elasticbox.session import AuthenticatedSession


def initialize_parser(subparsers):
    parser = subparsers.add_parser('run', help='Start a box inside a container')
    parser.add_argument('--install', action='store_true', dest='install')
    parser.add_argument('--instance-id', required=False, default=os.getenv('INSTANCE_ID', 'local'), dest='instance_id')
    parser.set_defaults(func=execute_command)


def execute_command(args):
    if args.token:
        session = AuthenticatedSession(args)
    else:
        session = None

    instance = Instance(args.instance_id, session)

    def stop_agent(_signum, _frame):
        instance.execute_event('stop')
        instance.execute_event('dispose')
        sys.exit(0)

    if 'install' in args and args.install:
        instance.execute_event('install')

    instance.execute_event('configure')
    instance.execute_event('start')

    signal.signal(signal.SIGINT, stop_agent)
    signal.signal(signal.SIGTERM, stop_agent)

    while True:
        time.sleep(1)
