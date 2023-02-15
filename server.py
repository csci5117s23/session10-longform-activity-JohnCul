from flask import Flask, request, render_template, jsonify, session, redirect, url_for

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from datetime import datetime
import os
import psycopg2
##flask manages session data weirdly, session is a python dict

from db import *
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.secret_key=os.environ['SECRET_KEY']

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

## auth stuff
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    ## if we want to do something with the user, this is where we'd do it
    ## first time we know if its a new user, can change the redirect easily if its a new user
    session["user"] = token
    session['uid'] = token['userinfo']['sid']
    session['email'] = token['userinfo']['email']
    session['picture'] = token['userinfo']['picture']
    ## check session for if they are logged in, can do that in jinja and python
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )



## initialize database connection with the pool in db.py before doing anything
@app.before_first_request
def setup_db():
    setup()

## homepage
@app.route('/', methods=['GET'])
def home():
  return render_template('home.html') 

## tour
@app.route('/tour', methods=['GET'])
def tour():
  return render_template('tour.html') 
