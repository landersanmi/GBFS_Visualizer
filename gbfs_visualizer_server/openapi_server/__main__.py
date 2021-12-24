#!/usr/bin/env python3

import connexion

from google.oauth2 import id_token
from google.auth.transport import requests

from openapi_server import encoder

from flask import Flask, url_for, redirect, render_template, request
from flask_babel import Babel, gettext, ngettext
import os
import jinja2

import requests

import json

with open('../keys.json') as f:
  keys = json.load(f)
   
def main():
    openapi_path = './openapi/'
    app = connexion.FlaskApp(__name__, specification_dir=openapi_path, options={"swagger_ui": True, "serve_spec": True})
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'GBFS Visualizer | This API allows consulting open data in a visual way from the different gbfs systems.'},
                pythonic_params=True)
    
    #babel = Babel(app)

    @app.route('/login')
    def maint():
        token = request.args.get('token', default = 'noToken', type = str)
        return redirect(url_for('map', token= str(token)))

    @app.route('/map')
    def map():
        token = request.args.get('token', default = 'noToken', type = str)
        # Specify the CLIENT_ID of the app that accesses the backend:
        response = requests.get('https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=' + token)
        
        if(response.status_code == 200):
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            print("CALL TO /MAP")
            return render_template('map.html', MAPS_API_KEY=keys["MAPS_API_KEY"])
        else: 
            # Invalid token
            print("BACK TO LOGIN")
            return redirect('http://127.0.0.1:9090/')



    app.run(port=8080)

    
if __name__ == '__main__':
    main()
