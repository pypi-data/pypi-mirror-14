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
import socket

from elasticbox.template import render


class Context(dict):

    def __init__(self, box_id, scope, instance, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

        self._box_id = box_id
        self._scope = scope
        self._instance = instance
        self._nested_boxes = []

        self._initialize_variables()
        self._assign_instance_variables()
        self._add_service_properties()
        self._add_context_properties()
        self._render_template_variables()

    def get_scope(self):
        return self._scope

    def get_box_id(self):
        return self._box_id

    def get_nested_boxes(self):
        return self._nested_boxes

    def _initialize_variables(self):
        scoped_variables = []

        for variable in self._instance.get_box(self._box_id)['variables']:
            name = variable['name']

            if variable['type'] == 'Box':
                if self._scope:
                    self[name] = Context(variable['value'], "{0}.{1}".format(self._scope, name), self._instance)
                else:
                    self[name] = Context(variable['value'], name, self._instance)

                self._nested_boxes.append(self[name])

            elif variable['type'] == 'Binding':
                self[name] = self._get_binding(name)

            elif 'scope' not in variable:
                self[name] = variable['value']

            else:
                scoped_variables.append(variable)

            if variable['type'] == 'File':
                self[name] = self._instance.get_location(self._box_id, variable['value'])

        # Process scoped variables
        for variable in scoped_variables:
            name = variable['name']

            # Initialize with the root scope
            scope = self

            # Walk the scope tree and create if does not exists
            for scope_name in variable['scope'].split('.'):
                scope = scope[scope_name]

            # Update variable value
            scope[name] = variable['value']

    def _assign_instance_variables(self):
        for variable in self._instance.get_variables():
            segments = variable['name'].split('.')
            name = segments.pop()

            # Initialize with the root scope
            scope = self

            # Walk the scope tree and create if does not exists
            for segment in segments:
                if segment in scope:
                    scope = scope[segment]

            # Update variable value
            if name in scope and variable['type'] != 'Binding':
                scope[name] = variable['value']

    def _add_service_properties(self):
        service = self._instance.get_service()

        self['addresses'] = service['addresses']
        if service['addresses']:
            self['address'] = service['addresses'][0]

    def _add_context_properties(self):
        self['folder'] = os.path.join('/var/elasticbox', self._instance.get_id())
        self['variables'] = self.copy()

        if not os.path.exists(self['folder']):
            os.makedirs(self['folder'])

    def _get_binding(self, name):
        if self._scope:
            path = '{0}.{1}'.format(self._scope, name)
        else:
            path = '{0}'.format(name)

        if os.environ.get('{0}_NAME'.format(path.upper())):
            addresses = []

            # Check for docker compose addresses
            count = 1
            while os.environ.get("{0}_{1}_NAME".format(path.upper(), count)):
                hostname = "{0}_{1}".format(path, count)
                addresses.append({"private": socket.gethostbyname(hostname)})
                count += 1

            # Fallback to standalone links
            if len(addresses) == 0:
                addresses.append({"private": socket.gethostbyname(path)})

            return {
                "address": addresses[0],
                "addresses": addresses
            }
        else:
            return []

    def _render_template_variables(self):
        for variable in self._instance.get_box(self._box_id)['variables']:
            name = variable['name']

            if variable['type'] == 'Box' or variable['type'] == 'Binding' or not variable['value']:
                continue

            if 'scope' not in variable:
                self[name] = render(self[name], self)
            else:
                # Initialize the scope tree
                scope = self

                # Walk the scope tree and create if does not exists
                for scope_name in variable['scope'].split('.'):
                    scope = scope[scope_name]

                # Update variable value
                scope[name] = render(scope[name], self)

    @staticmethod
    def _find_variable(name, variables):
        for variable in variables:
            if variable['name'] == name:
                return variable
