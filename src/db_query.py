from db_classes import db_session, start_session, MISSING, FOUND



def insert_missing(data, db_session = db_session):

	#To-Do handle repetition 

	#create new instance for db
	new_missing = MISSING(
						img_path = data['img_path'],
						name = data['name'],
						nationality = data['nationality'],
						description = data['description'],
						contact_name = data['contact_name'],
						contact_email = data['contact_email'],
						contact_phone = data['contact_phone'],
						)

	person_filed_found = query_found_by_name(data['name'])

	#push to db
	db_session.add(new_missing)
	db_session.commit()

	#if this person has been filed as a missing person, return data to contact family
	if person_filed_found:
		return person_filed_found

	#success
	return True


def query_missing_by_name(target_name, db_session = db_session):

	#search current db for instance with same name
	existing = db_session.query(MISSING).filter_by(name=target_name).first()

	return existing




def insert_found(data, db_session = db_session):

	#To-Do handle repetition 

	#create new instance for db
	new_found = FOUND(
						img_path = data['img_path'],
						name = data['name'],
						nationality = data['nationality'],
						description = data['description'],
						checkin_time = data['checkin_time'],
						location = data['location'],
						)

	person_filed_missing = query_missing_by_name(data['name'])

	#To-Do: Watson Image Recongition Check?

	#push to db
	db_session.add(new_found)
	db_session.commit()

	#if this person has been filed as a missing person, return data to contact family
	if person_filed_missing:
		return person_filed_missing

	#success
	return True


def query_found_by_name(target_name, db_session = db_session):

	#search current db for instance with same name
	existing = db_session.query(FOUND).filter_by(name=target_name).first()

	return existing




'''
data = {

	"img_path": "test1",
	"name": "test1",
	"nationality": "test1",
	"description": "test1",
	"checkin_time": "test1",
	"contact_email": "test1",
	"location": "test1",

}

status = insert_found(data)

print (status)
'''