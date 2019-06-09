import requests
import json


with open ("../config/config.json") as secret:
    credentials = json.load(secret)





def send_email(to_address, subject, message = None, html = None):

    #Load sandbox credentials

    request_link = credentials['mailguninbox']['sandbox_req_url']
    api = credentials['mailguninbox']['sandbox_api']
    from_id = credentials['mailguninbox']['sandbox_from_id']

    req = requests.post(
        request_link,
        auth=("api", api),
        data={"from": from_id,
                "to": [to_address],
                "h:Reply-To" : "support@reuniteai.com",
                "subject": subject,
                "text": message,
                "html": html
             }
        )

    return req.status_code


#send_email("jockonarock94@gmail.com","Missing Person Found", message= "Anand has been found.")