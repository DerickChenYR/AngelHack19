#!/usr/bin/python3.6
#Flask App for Reunite, AngelHack 19 NY

from flask import Flask, render_template, redirect, request, url_for, session, send_from_directory, abort
from werkzeug import secure_filename
import os
import sys
from datetime import datetime,timedelta
import json
import random
import traceback


#Load script files
from db_classes import db
from db_query import insert_found, insert_missing, query_missing_by_name, query_found_by_name

with open ("../config/config.json") as secret:
	credentials = json.load(secret)




server = Flask(__name__,template_folder='../templates')

WTF_CSRF_ENABLED = True
server.secret_key = os.urandom(999)


#Environment/Debugging Mode Setting
#ENV = 'production'/'development', single quotes needed
server.config["ENV"] = 'development'
server.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
	username=credentials['sqlalchemy']['username'],
	password=credentials['sqlalchemy']['password'],
	hostname=credentials['sqlalchemy']['hostname'],
	databasename=credentials['sqlalchemy']['databasename'],
)
server.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
server.config["SQLALCHEMY_POOL_RECYCLE"] = 60
server.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["PHOTO_UPLOAD_DIR"] = "../static/photos"

db.init_app(server)



#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

@server.route("/", methods=["GET"])
def index():

	if request.method == "GET":

		return render_template("index.html")

	else:
		abort(400) #bad request




@server.route("/checkin", methods=["GET","POST"])
def checkin():

	if request.method == "GET":

		return render_template("checkin.html")

	elif request.method == "POST":

		#img = request.files['file']

		#img_save_path = os.path.join(app.config['PHOTO_UPLOAD_DIR'], secure_filename(f.filename))

		#img.save(img_save_path)

		data = {
			"img_path": "test_path", #img_save_path,
			"name": request.form["name"],
			"nationality": request.form["nationality"],
			"description": request.form["description"],
			"checkin_time": request.form["checkin_time"],
			"location": request.form["location"],
		}

		response = insert_found(data)

		if response == True:
			return render_template("checkin.html", msg="Recorded New Found Person. This person has not been reported as missing.")
		else:
			return render_template("checkin.html", msg="Recorded New Found Person. This person was reported missing by {}, contact no. {}, contact eamil {}.".format(response.contact_name, response.contact_phone, response.contact_email))
	else:
		abort(400) #bad request




@server.route("/findmissing1", methods=["GET","POST"])
def findmissing1():

	if request.method == "GET":

		return render_template("findmissing1.html")

	elif request.method == "POST":

		img = request.files['file']

		img_save_path = os.path.join(server.config['PHOTO_UPLOAD_DIR'], secure_filename(img.filename))
		session['img_save_path'] = img_save_path

		img.save(img_save_path)
		return redirect(url_for("findmissing2"))

	else:
		abort(400) #bad request


@server.route("/findmissing2", methods=["GET","POST"])
def findmissing2():

	if request.method == "GET":

		return render_template("findmissing2.html")

	elif request.method == "POST":

		data = {
			"img_path": session['img_save_path'],
			"name": request.form["name"],
			"nationality": request.form["nationality"],
			"description": request.form["description"],
			"contact_name": request.form["contact_name"],
			"contact_phone": request.form["contact_phone"],
			"contact_email": request.form["contact_email"],
		}

		response = insert_missing(data)

		if response == True:
			return render_template("findmissing2.html", msg="Recorded New Missing Person. You will be contacted once this person has been found.")
		else:
			return ("failed")

	else:
		print(request.method)
	



if __name__ == "__main__":
	#app.run()
	server.run()
