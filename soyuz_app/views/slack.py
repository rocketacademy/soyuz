from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from ..models import Batch, Section
from django.contrib.auth import get_user_model
import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=settings.SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN


def create_channel(section, channel_name):
    try:
        # Call the conversations.create method using the WebClient
        # conversations_create requires the channels:manage bot scope
        result = client.conversations_create(
            # The name of the conversation
            name=channel_name
        )
        print('result', result)

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))

    # set and update slack_channel_id
    section.slack_channel_id = result["channel"]["id"]
    section.save()

# no longer needed


def lookup_by_email(user, user_list):
    try:
        email_lookup_result = client.users_lookupByEmail(
            email=user.email
        )
        print('email lookup result', email_lookup_result)

    except SlackApiError as e:
        logger.error("Error looking up email: {}".format(e))

    # save slack id if user is found in workspace and does not have a slack id
    if email_lookup_result["ok"]:
        if user.slack_id is None:
            user.slack_id = email_lookup_result["user"]["id"]
            user.save()

        if user_list is not None:
            user_list.append(user)

    else:
        print(email_lookup_result["error"])
        # TODO: send reminder email to student


def add_users_to_channel(section, id_string):
    try:
        add_user_result = client.conversations_invite(
            channel=section.slack_channel_id,
            users=id_string
        )
        print('add user result', add_user_result)

    except SlackApiError as e:
        logger.error("Error inviting user: {}".format(e))


def remove_from_channel(section, id_string):
    try:
        remove_user_result = client.conversations_kick(
            channel=section.slack_channel_id,
            user=id_string
        )
        print('remove_user_result', remove_user_result)

    except SlackApiError as e:
        logger.error("Error removing user: {}".format(e))


# slack events api verification
@csrf_exempt
def event_hook(request):
    json_dict = json.loads(request.body.decode('utf-8'))
    # slack events api url verification
    if json_dict['token'] != SLACK_VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    # return the challenge code here
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    # receiving a request from slack
    if 'event' in json_dict:
        event_obj = json_dict['event']
        # team_join event occured in slack workspace
        if ('type' in event_obj) and (event_obj['type'] == 'team_join'):
            # get user email from event obj
            user_email = event_obj['user']['profile']['email']
            # use email to query for user's batch
            user_batch = Batch.objects.get(users__email=user_email)
            # get user's slack id from event obj
            slack_id = event_obj['user']['id']
            # add slack id to user details
            user = get_user_model().objects.get(email=user_email)
            user.slack_id = slack_id
            user.save()
            # add user to batch slack channel
            add_users_to_channel(user_batch, slack_id)
            return HttpResponse(status=200)
    return HttpResponse(status=200)
