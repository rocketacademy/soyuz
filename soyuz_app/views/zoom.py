import jwt
import requests
import json
from time import time
from django.conf import settings


ZOOM_API_KEY = settings.ZOOM_API_KEY
ZOOM_API_SECRET = settings.ZOOM_API_SECRET


# generate jwt token using jwt library
def generate_token():
    token = jwt.encode(
        # Create token payload
        {'iss': ZOOM_API_KEY, 'exp': time() + 5000},
        # Secret used to generate token signature
        ZOOM_API_SECRET,
        # Specify the hashing algo
        algorithm='HS256'
    )
    return token


# create json data for post requests
# TODO: add alternative hosts!!
meeting_details = {"topic": "test meeting",
                   "type": 3,
                   "settings": {
                       "host_video": "true",
                       "participant_video": "true",
                       "join_before_host": "true",
                       "jbh_time": 0,
                       "mute_upon_entry": "false",
                       "use_pmi": "false",
                       "audio": "both",
                       "auto_recording": "cloud"
                   }
                   }


# send request with headers
def create_room(host_email):
    print(host_email)
    headers = {'authorization': 'Bearer %s' % generate_token(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/{host_email}/meetings',
        headers=headers, data=json.dumps(meeting_details))

    print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    id = y["id"]

    return id
