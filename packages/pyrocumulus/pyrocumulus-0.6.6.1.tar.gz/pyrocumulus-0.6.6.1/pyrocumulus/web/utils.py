# -*- coding: utf-8 -*-

# Copyright 2015 Juca Crispim <juca@poraodojuca.net>

# This file is part of pyrocumulus.

# pyrocumulus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyrocumulus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyrocumulus. If not, see <http://www.gnu.org/licenses/>.

from tornado.web import HTTPError
from pyrocumulus.utils import fqualname

# This ugly dict stores the handler classes and its allowed operations.
# Allowed operations are handled by request method, so this dict is used
# to know if a determined operation is valid for a request method
_allowed_operations = {}


def _create_allowed_operations(cls_fqualname):
    """Creates a skeleton for allowed operations in a class."""

    ops = {'get': {},
           'post': {},
           'put': {},
           'delete': {},
           'options': {},
           'inherited': False}

    _allowed_operations[cls_fqualname] = ops

    return _allowed_operations[cls_fqualname]


def inherit_operations(cls):
    """Inherits allowed operations from its super classes."""

    cls_fqualname = fqualname(cls)

    try:
        ops = _allowed_operations[cls_fqualname]
    except KeyError:
        # Wasn't created yet.
        _create_allowed_operations(cls_fqualname)
        ops = _allowed_operations[cls_fqualname]

    if ops['inherited']:
        return

    initial_ops = {'get': {},
                   'post': {},
                   'put': {},
                   'delete': {},
                   'options': {},
                   'inherited': False}

    bases = list(cls.__mro__)
    bases.reverse()
    for base in bases:
        base_fqualname = fqualname(base)
        base_ops = _allowed_operations.get(base_fqualname)
        if base_ops:
            base_get = base_ops['get']
            base_post = base_ops['post']
            base_put = base_ops['put']
            base_delete = base_ops['delete']
            base_options = base_ops['options']

            initial_ops['get'].update(base_get)
            initial_ops['post'].update(base_post)
            initial_ops['put'].update(base_put)
            initial_ops['delete'].update(base_delete)
            initial_ops['options'].update(base_options)

    initial_ops['get'].update(ops['get'])
    initial_ops['post'].update(ops['post'])
    initial_ops['put'].update(ops['put'])
    initial_ops['delete'].update(ops['delete'])
    initial_ops['options'].update(ops['options'])
    initial_ops['inherited'] = True
    _allowed_operations[cls_fqualname] = initial_ops


def set_operation(cls_fqualname, req_method, operation, cls_meth):
    """ Set ``operation`` as an allowed operation for ``cls`` using
    ``req_method``. Using this operation will trigger ``call``. """

    fqualname = cls_fqualname
    if fqualname not in _allowed_operations.keys():
        allowed = _create_allowed_operations(fqualname)
    else:
        allowed = _allowed_operations[fqualname]

    try:
        allowed[req_method].update({operation: cls_meth})
    except KeyError:
        msg = 'Request method {} not known!'.format(req_method)
        raise KeyError(msg)


def validate(req_type, cls, operation):
    """Validates if an operation is valid for a given request method.
    If the operation is valid returns the operation's method.

    """

    cls_fqualname = fqualname(cls)
    all_reqs = _allowed_operations.get(cls_fqualname)
    if not all_reqs:
        _create_allowed_operations(cls_fqualname)
        inherit_operations(cls)
        all_reqs = _allowed_operations[cls_fqualname]

    allowed = all_reqs[req_type]

    cls_meth = None

    for req in all_reqs.values():
        for op, meth in allowed.items():
            if operation == op:
                cls_meth = meth
                break
        if cls_meth:
            break

    if not cls_meth:
        raise HTTPError(404)
    elif operation not in allowed:
        raise HTTPError(405)

    return cls_meth
