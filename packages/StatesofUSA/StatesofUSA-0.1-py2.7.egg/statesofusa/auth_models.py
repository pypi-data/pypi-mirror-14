#!/usr/bin/env python

__author__ = 'Isham'

# Hardcoding client tokens for convinience.
USER_TOKEN_DICT = {
    'user1' : "8590ae64-74e0-480a-a3ff-b676e4d0e9aa",
    'user2' : "38c50d14-436b-4e3e-b447-e2e9334fea1a"
}



class Token(object):
    """
        Class to handle client tokens.
    """
    
    def __init__(self, usr, tok):
        self.user = usr
        self.token = tok
    
    @staticmethod
    def get( token):
        # creates a token object from the token string passed
        # Returns None on faulty tokens.
        token_object = None
        for client_name, client_token in USER_TOKEN_DICT.items():
            if client_token == token:
                token_object = Token(client_name, client_token)
        return token_object
    
