#!/usr/bin/python3.6
#DB Classes

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

import json

with open ("../config/config.json") as secret:
    credentials = json.load(secret)
    