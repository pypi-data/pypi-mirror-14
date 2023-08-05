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
import yaml

_boxes_path = os.path.join(os.getenv('ELASTICBOX_PATH'), 'boxes')


def _initialize_index():
    box_index = dict()

    if not os.path.exists(_boxes_path):
        os.makedirs(_boxes_path)

    for item in os.listdir(_boxes_path):
        box_path = os.path.join(_boxes_path, item, 'box.yaml')

        if os.path.exists(box_path):
            with open(box_path, 'r') as box_file:
                box = yaml.load(box_file)
                box_index[box['id']] = box

    return box_index


class Box(object):
    __box_index = _initialize_index()

    @staticmethod
    def load_box(box_ref):
        if box_ref in Box.__box_index:
            return Box.__box_index[box_ref]
        else:
            for box in Box.__box_index.values():
                if box['name'] == box_ref:
                    return box

        raise Exception("Box '%s' not found." % box_ref)

    @staticmethod
    def get_path(box_id, *args):
        box = Box.load_box(box_id)

        path = os.path.join(_boxes_path, box['name'], *args)
        if not os.path.exists(path):
            os.makedirs(path)

        return path
