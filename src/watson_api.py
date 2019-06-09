import json
from watson_developer_cloud import VisualRecognitionV3

from pprint import pprint

with open ("../config/config.json") as secret:
	credentials = json.load(secret)


#Return boolean if input image is Anand's
def watson_test(img_path):

	
	visual_recognition = VisualRecognitionV3(
			version='2018-03-19',
			iam_apikey=credentials['watson_API']['API_key']
	)

	score = None
	threshold = 0.3

	with open(img_path, 'rb') as images_file:
		classes = visual_recognition.classify(
		images_file,
		threshold="{}".format(threshold),
		classifier_ids="DefaultCustomModel_549148796"
		).get_result()
		pprint(classes)

		#get AI facial class model 2 scores
		try:
			score = float((json.dumps(classes["images"][0]["classifiers"][0]["classes"][0]["score"])))
		#score below threshold
		except:
			return False

	return score > threshold




