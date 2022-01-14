import jwt
import requests
import json
from time import time
from django.conf import settings

ZOOM_API_KEY = settings.ZOOM_API_KEY
ZOOM_API_SECRET = settings.ZOOM_API_SECRET


class Zoom:
    def __init__(self):
        # # generate jwt token using jwt library
        self.token = jwt.encode(
            # Create token payload
            {'iss': ZOOM_API_KEY, 'exp': time() + 5000},
            # Secret used to generate token signature
            ZOOM_API_SECRET,
            # Specify the hashing algo
            algorithm='HS256'
        )

        self.headers = {
            'authorization': f'Bearer {self.token}',
            'content-type': 'application/json'
        }

    def create_room(self, host_email, batch, section):
        host_email = 'michelle@rocketacademy.co'

        # create json data for post requests
        # TODO: add alternative hosts!!
        meeting_topic = f'{batch.course.name}-{batch.number}-{section.number}'
        meeting_details = {
            "topic": meeting_topic,
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

        r = requests.post(
            f'https://api.zoom.us/v2/users/{host_email}/meetings',
            headers=self.headers,
            data=json.dumps(meeting_details)
        )

        print(r.text)
        # converting the output into json and extracting the details
        y = json.loads(r.text)
        id = y["id"]

        return id

    def delete_recording(self, uuid):

        recording_details = {
            "action": "trash"
        }

        r = requests.delete(
            f'https://api.zoom.us/v2/meetings/{uuid}/recordings',
            headers=self.headers,
            data=json.dumps(recording_details)
        )

        print(r.text)
