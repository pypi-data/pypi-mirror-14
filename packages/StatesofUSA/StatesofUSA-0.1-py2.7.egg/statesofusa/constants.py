#!/usr/bin/env python

__author__ = 'Isham'

# Constants used throughout 

KEY_PAGE_NUM = 'page'
KEY_ITEMS_PER_PAGE = 'items_per_page'
KEY_AVAILABLE_PAGES = 'available_pages'

API_RESULT_DATA_TEMPLATE = {
    'result': '',
    'meta': {
        KEY_PAGE_NUM : '',
        KEY_ITEMS_PER_PAGE : '',
        KEY_AVAILABLE_PAGES : ''
    }
}


class ErrorMessages(object):
    NOT_ALLOWED = "This method is not allowed."
    HEADER_ERROR = "HTTP Header `Authorization` is not passed."
    TOKEN_ERROR = "The `Token` keyword on HTTP Header `Authorization` is not passed."
    INVALID_HEADER = "Invalid token header. No credentials provided."
    INVALID_TOKEN = "Invalid token."
    
class Status(object):
    SUCCESS = "success"
    FAILURE = "failure"
    
class ValidationTypes(object):
    NONE = ''
    NOT_ALLOWED = "NOT_ALLOWED"
    AUTHORIZATION = "AUTHORIZATION"
    URL_ERROR = "URL_NOT_FOUND"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"

