#!/usr/bin/python3.6
#DB Classes

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

import json


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

DB_LOCAL_PATH = "reunite"
SQLALCHEMY_DATABASE_PATH = 'sqlite:///' + DB_LOCAL_PATH

engine = create_engine(SQLALCHEMY_DATABASE_PATH, poolclass=NullPool)
db_session = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))

def start_session():
    engine = create_engine(SQLALCHEMY_DATABASE_PATH, poolclass=NullPool)
    db_session = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))
    return db_session


class MISSING(db.Model):

	__tablename__ = "missing"

	img_path = db.Column(db.TEXT)
	name = db.Column(db.TEXT, primary_key = True)
	nationality = db.Column(db.TEXT)
	description = db.Column(db.TEXT)
	contact_name = db.Column(db.TEXT)
	contact_email = db.Column(db.TEXT)
	contact_phone = db.Column(db.TEXT)



class FOUND(db.Model):

	__tablename__ = "found"

	img_path = db.Column(db.TEXT)
	name = db.Column(db.TEXT, primary_key = True)
	nationality = db.Column(db.TEXT)
	description = db.Column(db.TEXT)
	checkin_time = db.Column(db.TEXT)
	location = db.Column(db.TEXT)
