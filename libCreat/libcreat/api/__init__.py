# -*- coding: utf-8 -*-

from api_exception import APIError
from libcreat import model

def process_request(op_name, sid, params):
    result = {
        'info': 'success.',
        'data': {},
        'status': 0
    }

    try:
        op = op_dict[op_name]
    except KeyError as e:
        result['info'] = 'unknown api name [%s].' % e
        result['status'] = 2
        return result

    try:
        result['data'], result['info'] = op(sid, params)
    except APIError as e:
        result['info'] = e.info
        result['status'] = e.status
    except Exception as e:
        result['info'] = 'unknown server exception [%s].' % e
        result['status'] = 90
    return result

op_dict = {}
import inspect, sys

def load(mod):
    if '__all__' in mod.__dict__:
        names = mod.__all__
    else:
        names = dir(mod)
    if 'op_name' in names and 'process' in names:
        op_dict[mod.__dict__['op_name']] = mod.__dict__['process']


import spec_list
load(spec_list)

import spec_update
load(spec_update)

import spec_find
load(spec_find)

import spec_add
load(spec_add)

import tag_list
load(tag_list)

import tag_add
load(tag_add)

import tag_delete
load(tag_delete)

import update_no_lib
load(update_no_lib)

import spec_delete
load(spec_delete)