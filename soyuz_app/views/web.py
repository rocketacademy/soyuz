from ..models import Batch, Course, Section
from ..forms import AddBatchForm
from .slack import add_users_to_channel, create_channel, lookup_by_email, remove_from_channel
import math
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=settings.SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["GET", "POST"])
def get_batches(request):
    batches = Batch.objects.all()

    if request.method == "GET":
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {"title": "List of Batches", "batches": batches, "form": add_batch_form}
    return render(request, "batch-page.html", context)


@staff_member_required
@require_POST
def add_to_batch(request):
    batch_id = int(request.POST.get("batch_id"))
    user_id = int(request.POST.get("user_id"))

    destination_batch = Batch.objects.get(id=batch_id)
    user = get_user_model().objects.get(id=user_id)

    destination_batch.users.add(user)

    return redirect("soyuz_app:get_student_list")


@staff_member_required
@require_GET
def get_student_list(request):
    # getting users that are in a batch
    users = get_user_model().objects.filter(
        batch__isnull=False, is_superuser=False, is_staff=False
    )

    # getting users who do not belong in any batch
    users_no_batch = get_user_model().objects.filter(
        batch__isnull=True, is_superuser=False, is_staff=False
    )

    # getting all batches
    batches = Batch.objects.all()
    context = {
        "title": "Student List",
        "users": users,
        "users_no_batch": users_no_batch,
        "batches": batches,
    }

    return render(request, "student-list.html", context)


@staff_member_required
@require_GET
def get_sections(request, course_name, batch_number):
    course = Course.objects.get(name=course_name)
    print("course", course)
    batch = Batch.objects.get(number=batch_number, course=course)
    print("batch", batch)
    no_section_users = get_user_model().objects.filter(
        batch=batch, section__isnull=True, slack_id__isnull=False, is_superuser=False, is_staff=False
    )
    print('no section', no_section_users)

    slack_unregistered = get_user_model().objects.filter(
        batch=batch, slack_id__isnull=True, is_superuser=False, is_staff=False
    )
    print('slack unregistered', slack_unregistered)

    sections = batch.section_set.all()
    section_array = []
    for section in sections:
        section_obj = {}
        section_obj["id"] = section.id
        section_obj["number"] = section.number
        section_users = section.users.all()
        section_obj["users"] = section_users
        section_array.append(section_obj)

    context = {
        "batch": batch,
        "sections": section_array,
        "no_section_users": no_section_users,
        "slack_unregistered": slack_unregistered
    }

    return render(request, "section-page.html", context)


@staff_member_required
@require_POST
def delete_from_batch(request):
    user_id = int(request.POST.get("user_id"))
    section_id = int(request.POST.get("section_id"))
    batch_id = int(request.POST.get("batch_id"))

    print(user_id)
    print(section_id)
    print(batch_id)
    user = get_user_model().objects.get(id=user_id)
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name
    section = Section.objects.get(id=section_id)

    section.users.remove(user)
    batch.users.remove(user)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def assign_sections_channels(request):
    # get batch id from form
    number_per_section = int(request.POST.get("number_per_section"))
    batch_id = int(request.POST.get("batch_id"))

    # get all users in batch
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name
    batch_users = list(get_user_model().objects.filter(batch=batch))

    # get number of users in batch
    number_of_users = len(batch_users)

    registered_batch_users = []
    # check if users are registered on slack
    for user in batch_users:
        lookup_by_email(user, registered_batch_users)

    # calculate number of sections required
    sections_required = math.ceil(number_of_users / number_per_section)

    # create required number of sections
    for i in range(sections_required):
        section = Section.objects.create(number=i + 1, batch=batch)

        # array of user ids to add to slack channel
        user_ids = []
        # for each section created
        for j in range(number_per_section):
            # add users to new sections
            if len(registered_batch_users) > 0:
                new_user = registered_batch_users.pop()
                section.users.add(new_user)
                user_ids.append(new_user.slack_id)

        print('user ids', user_ids)
        # create slack channel
        channel_name = f"{batch.course.name}-{batch.number}-{section.number}-testchannel"
        print('channel name', channel_name)
        create_channel(section, channel_name)

        # add users to slack channel
        add_users_to_channel(section, user_ids)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def check_slack_registration(request):
    batch_id = int(request.POST.get("batch_id"))
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name

    # get users in batch that have no slack id
    slack_unregistered = get_user_model().objects.filter(
        batch=batch, slack_id__isnull=True, is_superuser=False, is_staff=False
    )

    for user in slack_unregistered:
        lookup_by_email(user, None)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def create_batch_channel(request):
    batch_id = int(request.POST.get("batch_id"))
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name

    channel_name = f"{batch.course.name}-{batch.number}-all"
    create_channel(None, channel_name)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def reassign_sections(request):
    # data from form
    number_per_section = int(request.POST.get("number_per_section"))
    batch_id = int(request.POST.get("batch_id"))

    # get all users in batch
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name
    batch_users = list(get_user_model().objects.filter(batch=batch))
    # get number of users in batch
    number_of_users = len(batch_users)

    # get number of sections
    sections = Section.objects.filter(batch=batch)
    num_previous_sections = sections.count()

    # find out how many sections are needed
    number_of_sections = math.ceil(number_of_users / number_per_section)

    # create additional sections if required
    if num_previous_sections < number_of_sections:
        difference = number_of_sections - num_previous_sections
        for i in range(difference):
            Section.objects.create(number=i + 1 + num_previous_sections, batch=batch)

    # disassociate users from their original sections
    for section in sections:
        section.users.clear()

    # get current batch sections
    current_sections = Section.objects.filter(batch=batch)
    for section in current_sections:
        for j in range(number_per_section):
            # add users to new sections
            if len(batch_users) > 0:
                new_user = batch_users.pop()
                section.users.add(new_user)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def add_to_section(request):
    user_id = int(request.POST.get("user_id"))
    section_id = int(request.POST.get("section_id"))
    destination_section = Section.objects.get(id=section_id)
    batch_id = int(request.POST.get("batch_id"))
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name
    user = get_user_model().objects.get(id=user_id)
    destination_section.users.add(user)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
def delete_items(request):
    # Fetch user id and section name of user we want to remove from a section
    user_to_delete = request.POST.get("user_id")
    user_section = request.POST.get("section_id")
    batch_id = request.POST.get("batch_id")
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name

    # section that user is in
    selected_section = Section.objects.get(id=int(user_section))
    # # user that we want to delete
    user = get_user_model().objects.get(id=int(user_to_delete))
    selected_section.users.remove(user)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


@staff_member_required
@require_POST
# fetch destinaton section number and user id
def switch_sections(request):
    section_destination = request.POST.get("section_number")
    user_to_move = request.POST.get("user_id")
    batch_id = request.POST.get("batch_id")
    batch = Batch.objects.get(id=batch_id)
    batch_number = batch.number
    course_name = batch.course.name
    # user that we want to move
    selected_user = get_user_model().objects.get(id=int(user_to_move))
    # # user's original section
    user_section = Section.objects.get(users__id=int(user_to_move))
    # # user's destination section
    destination_section = Section.objects.get(id=int(section_destination))
    user_section.users.remove(selected_user)
    destination_section.users.add(selected_user)

    return redirect("soyuz_app:get_sections", course_name=course_name, batch_number=batch_number)


def landing_page(request):
    return render(request, "landing-page.html")
