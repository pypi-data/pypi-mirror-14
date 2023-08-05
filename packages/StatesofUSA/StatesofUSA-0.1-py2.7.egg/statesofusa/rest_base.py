#!/usr/bin/env python

__author__ = 'Isham'

from flask import request
from flask.views import MethodView
from flask_restful import reqparse, abort, Api, Resource
from utils import Status, ErrorMessages
from response import RestResponse
from auth import authenticate_token_user
import logging

class RESTBase(Resource):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self._request = None
        super(RESTBase, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        # Only POST api will be used. Therefore stopping all the other methods.
        data = request.args
        self.logger.debug(data)
        self.logger.info(ErrorMessages.NOT_ALLOWED)
        return RestResponse.get(Status.FAILURE, ValidationTypes.NOT_ALLOWED, ErrorMessages.NOT_ALLOWED)

    def put(self):
        self.logger.info(ErrorMessages.NOT_ALLOWED)
        return RestResponse.get(Status.FAILURE, ValidationTypes.NOT_ALLOWED, ErrorMessages.NOT_ALLOWED)

    def process_post(self, *args, **kwargs):
        message = 'This method should implemented in child class.'
        self.logger.error(message)
        raise NotImplementedError(message)

    def validate_post_parameters(self, request):
        """
            This function can be overriden by the inherting class
            to validate API specific post parameters
        """
        return (Status.SUCCESS, None, None)


    def post(self, *args, **kwargs):
        
        data = None
        self._request = request
        status, _type, message = authenticate_token_user(request)
        if status == Status.FAILURE:
            return RestResponse.get(status, _type, message)

        if status != Status.FAILURE:
            (status, _type, message) = self.validate_post_parameters(request)
            if status != Status.FAILURE:
                (status, _type, message, data) = self.process_post(request)

        #try:
        if status == Status.FAILURE:
            log_message = "%s, POST %s" % (message, data)
            self.logger.warning(log_message, )
            return RestResponse.get(status, _type, data, message)


        log_message = "%s, POST %s" % (message, data)
        self.logger.debug(log_message)
        return RestResponse.get(status, _type, message, result=data )
    
