from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from ..models import Batch, Section
import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=settings.SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


@require_POST
def create_channels(request):

    batch_id = int(request.POST.get("batch_id"))

    batch = Batch.objects.get(id=batch_id)
    sections = Section.objects.filter(batch=batch)

    for section in sections:
        if section.users.count() > 0:
            channel_name = f"{batch.course.name}-{batch.number}-{section.number}-testing"

            try:
                # Call the conversations.create method using the WebClient
                # conversations_create requires the channels:manage bot scope
                result = client.conversations_create(
                    # The name of the conversation
                    name=channel_name
                )

                # set and update slack_channel_id
                section.slack_channel_id = result["channel"]["id"]
                section.save()

                section_users = get_user_model().objects.filter(section=section)
                # string that will be used in slack api call (users)
                slack_user_ids = ""
                for user in section_users:
                    # function that looks up user emails on slack(gets slack user ids)
                    lookup_by_email(user, slack_user_ids)
                # function that adds user to channel
                add_user_to_channel(section, slack_user_ids)

            except SlackApiError as e:
                logger.error("Error creating conversation: {}".format(e))

    return redirect("soyuz_app:get_sections", course_name=batch.course.name, batch_number=batch.number)


def lookup_by_email(user):
    id_string = ''
    try:
        email_lookup_result = client.users_lookupByEmail(
            email=user.email
        )
        print('email lookup result', email_lookup_result)

        if email_lookup_result["ok"]:
            id_string += email_lookup_result["user"]["id"]
        else:
            print(email_lookup_result["error"])

    except SlackApiError as e:
        logger.error("Error finding user: {}".format(e))

    return id_string


def add_user_to_channel(section, id_string):

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
