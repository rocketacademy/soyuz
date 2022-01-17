import json
import threading

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..library.slack import Slack
from ..models import Section, Batch

SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN

# slack events api verification


@csrf_exempt
@require_POST
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))

    # slack events api url verification
    if json_dict["token"] != SLACK_VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    # return the challenge code here
    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return JsonResponse(response_dict, safe=False)
    # receiving team_join notification from slack
    if "event" in json_dict:
        event_obj = json_dict["event"]

        # the slack webhook will fire again if status 200 is not sent back within 3 seconds

        # threading is used here because we want this code to run in the background
        t = threading.Thread(target=team_join_event, args=(event_obj,))
        t.start()

        return HttpResponse(status=200)


def team_join_event(event_obj):

    # get user email from event obj
    user_email = event_obj["user"]["profile"]["email"]
    # get user's slack id from event obj
    slack_id = event_obj["user"]["id"]
    try:
        user = get_user_model().objects.get(email=user_email)

    except get_user_model().DoesNotExist:
        print("User not registered on Soyuz")

    else:
        # add slack id to user details
        user.slack_id = slack_id
        user.save()

        slack_client = Slack()

        user_batches = user.batch_set.filter().order_by("-start_date")

        if len(user_batches) > 0:
            user_batch = user_batches[0]
            print('user batch', user_batch)

            slack_client.add_users_to_channel(user_batch, slack_id)

            try:
                user_section = user.section_set.get(batch=user_batch)
                print('user section', user_section)

            except Section.DoesNotExist:
                print('section does not exist')

            else:
                slack_client.add_users_to_channel(user_section, slack_id)
