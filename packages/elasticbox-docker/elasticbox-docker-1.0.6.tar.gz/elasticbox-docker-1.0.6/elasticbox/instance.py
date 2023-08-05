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
import stat
import subprocess
import sys
import tempfile

import yaml

from elasticbox.box import Box
from elasticbox.context import Context
from elasticbox.template import render


class Instance(object):

    def __init__(self, instance_id, session=None):
        self._session = session

        if session:
            self._instance = self._session.get('/services/instances/{0}', instance_id).json()
        else:
            instance_path = Instance.get_instance_filepath()
            if os.path.exists(instance_path):
                with open(instance_path, 'r') as instance_file:
                    self._instance = yaml.load(instance_file)
            else:
                raise Exception('Instance file not found.')

            self._instance['id'] = instance_id

            if 'variables' not in self._instance:
                self._instance['variables'] = []

            for name, value in os.environ.iteritems():
                self._instance['variables'].append({'name': name, 'value': value, 'type': 'Text'})

    def get_id(self):
        return self._instance['id']

    def get_variables(self):
        return self._instance.get('variables')

    def get_location(self, box_id, path):
        if self._session:
            return os.getenv('ELASTICBOX_URL', 'elasticbox.com') + path
        else:
            box = self.get_box(box_id)
            return 'file://{0}/{1}/{2}'.format(os.path.join(os.getenv('ELASTICBOX_PATH'), 'boxes'), box['name'], path)

    def get_box(self, box_id=None):
        if box_id is None:
            box_id = self._instance['box']

        if 'boxes' in self._instance:
            for box in self._instance['boxes']:
                if box['id'] == box_id or ('version' in box and box['version']['box'] == box_id):
                    return box
        else:
            return Box.load_box(box_id)

    def get_service(self):
        if self._session:
            service = self._session.get('/services/instances/{0}/service', self._instance['id']).json()

            addresses = []
            for machine in service['machines']:
                addresses.append(machine['address'])

            return {
                'address': addresses[0] if addresses else None,
                'addresses': addresses,
            }
        else:
            _, _, addresses = socket.gethostbyname_ex(socket.gethostname())

            return {
                'address': [{'private': addresses[0]}],
                'addresses': [{'private': address} for address in addresses],
            }

    def set(self, name, value, scope):
        if self._session:
            data = {'name': name, 'box': scope}
            self._session.post('/services/instances/{0}/set', self._instance['id'], json=data)
        else:
            found = False

            instance_path = Instance.get_instance_filepath()
            if os.path.exists(instance_path):
                with open(instance_path, 'r') as instance_file:
                    instance = yaml.load(instance_file)
            else:
                raise Exception('Instance file not found.')

            if 'variables' not in instance:
                instance['variables'] = []

            if scope:
                full_name = "{0}.{1}".format(scope, name)
            else:
                full_name = name

            for variable in instance['variables']:
                if variable['name'] == full_name:
                    variable['value'] = value
                    found = True

            if not found:
                variable = {'name': full_name, 'value': value, 'type': 'Text'}
                instance['variables'].append(variable)

            Instance.persist(instance)

    def config(self, template, scope, context=None):
        if self._session:
            data = {
                'machine': {'address': {'private': socket.gethostbyname(socket.gethostname())}},
                'engines': ['jinja2', 'velocity'],
                'box': context.get_scope() if context else scope,
                'template': template
            }

            response = self._session.post(
                '/services/instances/{0}/config',
                self._instance['id'],
                json=data)

            return response.text
        else:
            if not context:
                context = Context(self._instance['box'], None, self)

            # Walk the scope tree
            if scope:
                for name in scope.split('.'):
                    if name in context:
                        context = context[name]
                    else:
                        raise Exception('Scope {0} not found.'.format(scope))

            return render(template, context)

    def execute_event(self, event_name):
        self._execute_event(Context(self.get_box()['id'], None, self), event_name)

    def _execute_event(self, context, event_name):
        events_dir = Box.get_path(context.get_box_id(), 'events')

        if event_name in ['install', 'configure', 'start']:
            before_script = os.path.join(events_dir, 'pre_{0}'.format(event_name))
        else:
            before_script = os.path.join(events_dir, event_name)

        if os.path.exists(before_script):
            result = self._execute_script(context, before_script)
            if result != 0:
                sys.exit(result)

        for box in context.get_nested_boxes():
            self._execute_event(box, event_name)

        if event_name in ['stop', 'dispose']:
            after_script = os.path.join(events_dir, 'post_{0}'.format(event_name))
        else:
            after_script = os.path.join(events_dir, event_name)

        if os.path.exists(after_script):
            result = self._execute_script(context, after_script)
            if result != 0:
                sys.exit(result)

    def _execute_script(self, context, script_file):
        filename = ''

        try:
            with tempfile.NamedTemporaryFile('w', delete=False) as script:
                filename = script.name

                with open(script_file, 'r') as template:
                    contents = template.read().decode('utf-8')
                    print >> script, self.config(contents, None, context=context)

            os.chmod(filename, stat.S_IXUSR)

            environment = os.environ.copy()
            if context.get_scope():
                environment['ELASTICBOX_SCOPE'] = context.get_scope()

            return subprocess.call(filename, cwd=self._get_instance_working_dir(), shell=True, env=environment)
        finally:
            os.remove(filename)

    def _get_instance_working_dir(self):
        instance_path = os.path.join(os.getenv('ELASTICBOX_INSTANCE_PATH'), self._instance['id'])

        if not os.path.exists(instance_path):
            os.makedirs(instance_path)

        return instance_path

    @staticmethod
    def initialize(box_id):
        path = os.getenv('ELASTICBOX_PATH')
        if not os.path.exists(path):
            os.makedirs(path)

        Instance.persist({'box': box_id})

    @staticmethod
    def get_instance_filepath():
        return os.path.join(os.getenv('ELASTICBOX_PATH'), 'instance.yml')

    @staticmethod
    def persist(instance):
        with open(Instance.get_instance_filepath(), 'wb') as instance_file:
            yaml.safe_dump(
                instance,
                stream=instance_file,
                encoding='utf-8',
                allow_unicode=True,
                default_flow_style=False)
