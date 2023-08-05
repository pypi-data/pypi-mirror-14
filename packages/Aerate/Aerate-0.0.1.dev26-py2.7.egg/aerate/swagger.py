# -*- coding: utf-8 -*-
"""
    swagger
    ~~~~~~~~~~~~~~~
    Handles importation and validation of the Aerate swagger specification

    :copyright: (c) 2016 by Kelly Caylor.
    :license: BSD, see LICENSE for more details.

"""
from bravado_core.spec import Spec
import json


class Swagger(object):

    def __init__(self, spec=None, config=None):
        self.spec_dict = None
        if spec:
            self.spec_dict = spec
        # TODO: Set defaults and read/set passed in config values.
        self.config = {
            'validate_requests': True,
            'validate_responses': True,
            'use_models': True,
        }
        if self.spec_dict:
            self.spec = Spec.from_dict(self.spec_dict, config=self.config)

    def _get_security(self, op_id=None):
        op = self._get_op_by_id(op_id)
        security = []
        if op and 'security' in op.op_spec:
            for item in op.op_spec['security']:
                # It's not our fault. The security is a list of dicts.
                security.append(list(item.keys())[0])
        elif 'security' in self.spec.spec_dict:
            # TODO: Handle this case of top-level security definitions
            # security.append(self.spec.spec_dict['security'].keys())
            pass
        return security

    def _get_op_id_list(self):
        op_id_list = []
        for resource in self.spec.resources.values():
            for op in resource.operations.values():
                if op \
                        and 'x-aerate-binding' in op.op_spec\
                        and op.op_spec['x-aerate-binding']:
                    op_id_list.append(op.op_spec['x-aerate-binding'])
        return op_id_list
        # print self.spec.resources[res][0]
        # print dir(self.spec.resources[res])
        # # op_id_list.append(dir(self.spec.resources[res]))
        # Flatten down the list of operationIds:
        # return list(chain.from_iterable(op_id_list))

    def _get_resource_list(self):
        return list(
            set([x.split('_')[0] for x in self._get_op_id_list()])
        )

    def _get_op_by_id(self, op_id):
        """
        Returns an bravado-core operation object correspoinding to a
        specific OperationId defined in the swagger spec.

        """
        op = None
        for resource in self.spec.resources.values():
            try:
                # op = getattr(resource, op_id)
                for oper in resource.operations.values():
                    if 'x-aerate-binding' in oper.op_spec \
                            and op_id == oper.op_spec['x-aerate-binding']:
                            return oper
            except AttributeError:
                pass  # maybe log this later
        return op

    def load_spec_from_file(self, filename):
        import os
        fileName, fileExtension = os.path.splitext(filename)
        if fileExtension == '.json':
            self.spec_dict = json.loads(open(filename, 'r').read())
        elif fileExtension == '.yaml':
            import yaml
            self.spec_dict = yaml.load(open(filename, 'r').read())
        else:
            raise TypeError("cannot detect filetype of {0}".format(filename))
        self.spec = Spec.from_dict(self.spec_dict, config=self.config)
        return True

    def load_spec_from_uri(self, uri):
        raise NotImplementedError()
