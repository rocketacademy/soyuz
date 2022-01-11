import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

ZOOM_API_KEY = settings.ZOOM_API_KEY
ZOOM_API_SECRET = settings.ZOOM_API_SECRET


@csrf_exempt
def zoom_webhook(request):
    json_dict = json.loads(request.body.decode('utf-8'))

    # if recording is complete
    if json_dict['event'] == 'recording.completed':
        recording_files = json_dict['payload']['object']['recording_files'][0]
        # get url of recording
        download_url = recording_files['download_url']
        play_url = recording_files['play_url']
        print('download_url', download_url)
        print('play url', play_url)

    return HttpResponse(status=200)
