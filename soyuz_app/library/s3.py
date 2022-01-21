from datetime import datetime

import boto3
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_BUCKET = settings.AWS_BUCKET
AWS_REGION = settings.AWS_REGION


@csrf_exempt
class S3:
    def __init__(self):

        self.session = boto3.Session()
        self.client = boto3.client("s3")

    def upload_video(self, url, json_dict):
        print("video uploading ............")
        r = requests.get(url, stream=True)

        bucket_name = AWS_BUCKET
        # creating file's name in s3 bucket
        meeting_topic = json_dict["payload"]["object"]["topic"]
        course_name = meeting_topic.split()[0]

        # include time to make filename unique
        date_time = datetime.now().strftime("%d-%m-%Y %H-%M")
        # key is the name of file on your bucket
        key = f"{course_name}/{meeting_topic}-{date_time}"

        s3 = self.session.resource("s3")
        bucket = s3.Bucket(bucket_name)
        bucket.upload_fileobj(r.raw, key, ExtraArgs={"ContentType": "video/mp4"})

        return f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
