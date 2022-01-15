# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
import logging

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.contrib.auth import get_user_model
from ..emails.reminder import send_reminder
from ..models import Batch
logger = logging.getLogger(__name__)


class Slack:
    def __init__(self):
        # WebClient insantiates a client that can call API methods
        self.client = WebClient(token=settings.SLACK_BOT_TOKEN)

    def create_channel(self, section, channel_name):
        try:
            # Call the conversations.create method using the WebClient
            # conversations_create requires the channels:manage bot scope
            result = self.client.conversations_create(
                # The name of the conversation
                name=channel_name
            )

        except SlackApiError as e:
            logger.error("Error creating conversation: {}".format(e))

        else:
            # set and update slack_channel_id
            section.slack_channel_id = result["channel"]["id"]
            section.save()

    # no longer needed after b13, slack registration is automated using webhook

    def lookup_by_email(self, user, user_list):
        try:
            email_lookup_result = self.client.users_lookupByEmail(email=user.email)
            print('emil', email_lookup_result)

        except SlackApiError as e:
            logger.error("Error looking up email: {}".format(e))

        else:
            # save slack id if user is found in workspace and does not have a slack id
            user.slack_id = email_lookup_result["user"]["id"]
            user.save()

            if user_list is not None:
                user_list.append(user)

        finally:
            var_exists = 'email_lookup_result' in locals() or 'email_lookup_result' in globals()
            if var_exists is False:
                batch = Batch.objects.get(users__email=user.email)
                send_reminder(user, batch)

    def add_users_to_channel(self, section, id_string):
        print('section', section)
        print('id ', id_string)

        try:
            add_user_result = self.client.conversations_invite(
                channel=section.slack_channel_id, users=id_string
            )

            return add_user_result

        except SlackApiError as e:
            logger.error("Error inviting user: {}".format(e))

    def remove_from_channel(self, section, id_string):
        try:
            remove_user_result = self.client.conversations_kick(
                channel=section.slack_channel_id, user=id_string
            )

            return remove_user_result

        except SlackApiError as e:
            logger.error("Error removing user: {}".format(e))

    def create_slack_channel(self, batch, section):
        # array of user ids to add to slack channel
        user_ids = []

        section_users = list(
            get_user_model().objects.filter(
                # slack id is needed to add user to slack channel
                section=section, slack_id__isnull=False, is_superuser=False, is_staff=False
            ))

        unregistered_users = list(
            get_user_model().objects.filter(
                # slack id is needed to add user to slack channel
                section=section, slack_id__isnull=True, is_superuser=False, is_staff=False
            )
        )

        if len(section_users) > 0:
            for user in section_users:
                user_ids.append(user.slack_id)

            # create slack channel only if there are slack registered students in the section
            if len(user_ids) > 0:
                channel_name = f"{batch.course.name}-{batch.number}-{section.number}-test"
                self.create_channel(section, channel_name)

                # add users to slack channel
                self.add_users_to_channel(section, user_ids)
        # send reminder email if user does not have a slack_id
        if len(unregistered_users) > 0:
            for user in unregistered_users:
                send_reminder(user, batch)
