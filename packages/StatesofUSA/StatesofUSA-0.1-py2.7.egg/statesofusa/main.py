#!/usr/bin/env python

__author__ = 'Isham'


from app import app, api
from us_states_api import USStates

api.add_resource(USStates, '/states/')


if __name__ == '__main__':
    app.run(debug=True)

