import logging

from django.conf import settings
from django.shortcuts import render
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from ..forms import AddBatchForm
from ..models import Batch, Section

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=settings.SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


def confirm_registration(request):
    return render(request, "registration_success.html")


def get_batches(request):
    batches = Batch.objects.all()
    print(batches)

    if request.method == "GET":
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {"title": "List of Batches", "batches": batches, "form": add_batch_form}
    return render(request, "batch-page.html", context)


def get_sections(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    sections = Section.objects.filter(batch_id=batch_id)
    users = batch.users.all()
    print(users)

    section_array = []
    for section in sections:
        section_obj = {}
        section_obj["number"] = section.number
        section_users = section.users.all()
        section_obj["users"] = section_users
        section_array.append(section_obj)

    if "create_channels" in request.POST:
        print("inside post request")
        try:
            # Call the conversations.create method using the WebClient
            # conversations_create requires the channels:manage bot scope
            result = client.conversations_create(
                # The name of the conversation
                name="soyuz-channel-1"
            )
            # Log the result which includes information like the ID of the conversation
            logger.info(result)

        except SlackApiError as e:
            logger.error("Error creating conversation: {}".format(e))

    context = {
        "title": "List of Sections",
        "batch": batch,
        "sections": section_array,
    }

    return render(request, "section-page.html", context)
