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

from string import Template  # pylint: disable=W0402

from jinja2 import Undefined
from jinja2.sandbox import SandboxedEnvironment


# pylint: disable=R0903,R0924
class SilentUndefined(Undefined):

    def __getitem__(self, _key):
        return self

    def __getattr__(self, _key):
        return self


def render(template, context):
    # Velocity style substitutions
    template = Template(template).safe_substitute(context)

    # Jinja style substitutions
    environment = SandboxedEnvironment(
        undefined=SilentUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True)

    return environment.from_string(template).render(context)
