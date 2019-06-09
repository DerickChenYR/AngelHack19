#!/usr/bin/python3.6
#Flask App for Reunite, AngelHack 19 NY

from flask import Flask, render_template, redirect, request, url_for, session, send_from_directory, abort
from werkzeug import secure_filename
import os
import sys
import time
import json
import random
import traceback
import base64
import hashlib


#Load script files
from db_classes import db
from db_query import insert_found, insert_missing, query_missing_by_name, query_found_by_name
from watson_api import watson_test
from alert_email import send_email


server = Flask(__name__,template_folder='../templates', static_folder='../static', static_url_path='/static')

WTF_CSRF_ENABLED = True
server.secret_key = os.urandom(999)



#Environment/Debugging Mode Setting
#ENV = 'production'/'development', single quotes needed
server.config["ENV"] = 'development'
server.config["DEBUG"] = True

server.config["SQLALCHEMY_DATABASE_URI"] = None
server.config["SQLALCHEMY_POOL_RECYCLE"] = 60
server.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["PHOTO_UPLOAD_DIR"] = "../static/photos"
server.config["STATIC_FOLDER"] = "../static/"

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



@server.route("/photo", methods=["POST"])
def photo():
	hash = hashlib.sha1()
	hash.update(str(time.time()).encode('utf-8'))

	filename = "{}.png".format(hash.hexdigest()[:10])

	img_save_path = os.path.join(server.config['PHOTO_UPLOAD_DIR'], filename)
	#img_save_path = os.path.join(server.config['PHOTO_UPLOAD_DIR'], "test.png")
	session['img_save_path'] = img_save_path


	image_64 = request.data
	image_data = base64.b64decode(image_64)

	with open(img_save_path, 'wb') as image:
		image.write(image_data)


	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



@server.route("/checkin1", methods=["GET","POST"])
def checkin1():

	if request.method == "GET":
		return render_template("checkin1.html")



@server.route("/checkin2", methods=["GET","POST"])
def checkin2():

	if request.method == "GET":
		return render_template("checkin2.html")

	elif request.method == "POST":

		data = {
			"img_path": session['img_save_path'],
			"name": request.form["name"],
			"nationality": request.form["nationality"],
			"description": request.form["description"],
			"checkin_time": request.form["checkin_time"],
			"location": request.form["location"],
		}

		response = insert_found(data)

		if response == True:
			return render_template("checkin2.html", msg="Recorded New Found Person. This person has not been reported as missing.")
		else:
			#A missing person of same name is on record, primary match key
			session["missing_name"] = response.name
			return redirect(url_for("checkin3"))
	else:
		abort(400) #bad request


@server.route("/checkinmissing", methods=["GET"])
def checkin3():

	if request.method == "GET":

		response = query_missing_by_name(session["missing_name"])

		#Check Waston AI, as secondary match key
		confidence = watson_test(session['img_save_path'])

		if type(confidence) is float:
			send_email(response.contact_email, "Missing Person Found", "We have found {} with {} confidence level.".format(response.name, confidence))
			return render_template("checkin3.html", facial_ai = "Matched", ai_confidence = confidence, name = response.name, contact_name=response.contact_name, contact_phone=response.contact_phone, contact_email=response.contact_email)
		else:
			return render_template("checkin3.html", facial_ai = "NOT Matched", ai_confidence = 0.0, name = response.name, contact_name=response.contact_name, contact_phone=response.contact_phone, contact_email=response.contact_email)
		


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

		session["searcher_email"] = request.form["contact_email"]

		response = insert_missing(data)

		if response == True:
			return render_template("findmissing2.html", msg="Recorded New Missing Person. You will be contacted once this person has been found.")
		else:
			session["found_name"] = response.name
			return redirect(url_for("findmissing3"))

	else:
		print(request.method)
	


@server.route("/findmissing3", methods=["GET"])
def findmissing3():

	if request.method == "GET":

		response = query_found_by_name(session["found_name"])

		#Check Waston AI, as secondary match key
		confidence = watson_test(session['img_save_path'])

		if type(confidence) is float:
			send_email(session["searcher_email"], "Missing Person Found", "We have found {} with {} confidence level.".format(response.name, confidence))
			return render_template("findmissing3.html", facial_ai = "Matched", ai_confidence = confidence, name = response.name, location = response.location)
		else:
			return render_template("findmissing3.html", facial_ai = "NOT Matched", ai_confidence = 0.0, name = response.name, location = response.location)
		


if __name__ == "__main__":
	#app.run()
	server.run()
