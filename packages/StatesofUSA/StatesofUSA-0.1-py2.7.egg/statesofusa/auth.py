#!/usr/bin/env python

__author__ = 'Isham'


import logging
from auth_models import Token
from constants import ErrorMessages, Status, ValidationTypes
logger = logging.getLogger(__name__)


def authenticate_token_user(request):
    """
        Handles the authentication of a client using predefined tokens.
    """
    token_key_header = request.headers.get('AUTHORIZATION')
    log_msg = "Request Header {0},  POST {1}".format(token_key_header, request.data)
    token_authentication = Status.FAILURE

    logger.info(log_msg)
    if token_key_header is None:
        message = ErrorMessages.HEADER_ERROR
        logger.error("Header information %s" % request.headers)
    else:
        auth = token_key_header.split()
        if not auth or auth[0].lower() !=b'token':
            message = ErrorMessages.TOKEN_ERROR
        elif len(auth) == 1:
            message = ErrorMessages.INVALID_TOKEN
        elif len(auth) > 2:
            message = ErrorMessages.INVALID_HEADER
        else:
            token_authentication = Status.SUCCESS

    if token_authentication == Status.SUCCESS:
        
        token_key = auth[1]
        token = Token.get(token=token_key)
    
        logger.info("Accepted Token for user %s" % token.user)

        if not token:
            message = ErrorMessages.INVALID_TOKEN

    if token_authentication == Status.FAILURE :
        msg = "{0}, {1}".format(log_msg, message)
        logger.warning(msg)
        return (Status.FAILURE, ValidationTypes.AUTHORIZATION, message)

    message = "Authentication Successful."

    return (Status.SUCCESS, None, message)
