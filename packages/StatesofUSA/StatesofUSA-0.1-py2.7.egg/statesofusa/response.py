#!/usr/bin/env python

__author__ = 'Isham'

from flask import jsonify
from app import app

class RestResponse(object):

    @classmethod
    def get(cls, status, _type, message, result=None, **kwargs):
        data = {'type': _type, 'status': status, 'message': message}
        if kwargs:
            data['additional_data'] = kwargs
        if result is not None:
            data['data'] = result
        content = jsonify(data)
        return app.make_response(content)
    
