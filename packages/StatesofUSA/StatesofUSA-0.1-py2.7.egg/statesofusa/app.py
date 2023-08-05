#!/usr/bin/env python

__author__ = 'Isham'

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
