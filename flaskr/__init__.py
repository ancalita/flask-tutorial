#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 15:54:19 2020

@author: pichon
"""

import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    @app.route('/hello')
    def hello():
        return 'Hello,World!'
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app

     