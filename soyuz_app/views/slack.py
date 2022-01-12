import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..library.slack import Slack
from ..models import Batch

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
    # receiving a request from slack
    if "event" in json_dict:
        event_obj = json_dict["event"]
        # team_join event occured in slack workspace
        if ("type" in event_obj) and (event_obj["type"] == "team_join"):
            # get user email from event obj
            user_email = event_obj["user"]["profile"]["email"]
            # use email to query for user's batch
            user_batch = Batch.objects.get(users__email=user_email)
            # get user's slack id from event obj
            slack_id = event_obj["user"]["id"]
            # add slack id to user details
            user = get_user_model().objects.get(email=user_email)
            user.slack_id = slack_id
            user.save()
            # add user to batch slack channel

            slack_client = Slack()
            slack_client.add_users_to_channel(user_batch, slack_id)
            return HttpResponse(status=200)
    return HttpResponse(status=200)
