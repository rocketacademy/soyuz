import json
import threading
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ..library.s3 import S3
from ..library.zoom import Zoom
from ..models import Section, Recording


@csrf_exempt
def recording_complete(request):
    json_dict = json.loads(request.body.decode('utf-8'))

    t = threading.Thread(target=upload_delete_recording, args=(json_dict,))
    t.start()

    return HttpResponse(status=200)


def upload_delete_recording(json_dict):
    # if recording is complete
    if json_dict['event'] == 'recording.completed':
        print('json dict', json_dict)
        print('recording complete')

        recording_files = json_dict['payload']['object']['recording_files']
        # download token provided in response sent by zoom needed to access video
        download_token = json_dict['download_token']
        # uuid needed to identify meeting to delete
        uuid = json_dict['payload']['object']['uuid']
        meeting_id = json_dict['payload']['object']['id']
        download_url = ''

        for file in recording_files:
            # there are 2 files in recording_files, M4A(audio only) and MP4(audio and video)
            if file['file_type'] == 'MP4':
                # get url of recording
                download_url = file['download_url']

        # this is the format the url needs to be presented in for us to be able to access the video
        url = f'{download_url}/?access_token={download_token}'

        s3_client = S3()
        aws_url = s3_client.upload_video(url, json_dict)

        print(aws_url)

        zoom_client = Zoom()
        zoom_client.delete_recording(uuid)

        # add entry into the recordings table
        print('finished delete')
        meeting_id = '86511015693'
        section = Section.objects.get(zoom_meeting_id=meeting_id)
        print('section ============ ', section)
        new_recording = Recording(url=aws_url, section=section)
        print('new recording', new_recording)
        new_recording.save()
