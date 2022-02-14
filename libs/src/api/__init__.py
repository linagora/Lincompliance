#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .package.resources import Packages

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
CORS(app)
api = Api(app)
api.add_resource(Packages, '/package')


@app.route('/')
def main():
    return 'Api up and running.', 200
