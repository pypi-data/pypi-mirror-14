#!/usr/bin/env python
"""
ElasticBox Confidential
Copyright (c) 2015 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""


from __future__ import absolute_import

import argparse
import os

import elasticbox.commands.config
import elasticbox.commands.run
import elasticbox.commands.set
import elasticbox.commands.setup


def main():
    parser = argparse.ArgumentParser(
        description='ElasticBox Agent commands',
        epilog="See 'elasticbox command --help' for more information")

    parser.add_argument('--token', required=False, default=os.getenv('ELASTICBOX_TOKEN', None), dest='token')
    parser.add_argument('--url', required=False, default=os.getenv('ELASTICBOX_URL', 'elasticbox.com'), dest='url')

    subparsers = parser.add_subparsers(title='Commands', dest='command')

    elasticbox.commands.setup.initialize_parser(subparsers)
    elasticbox.commands.config.initialize_parser(subparsers)
    elasticbox.commands.set.initialize_parser(subparsers)
    elasticbox.commands.run.initialize_parser(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
