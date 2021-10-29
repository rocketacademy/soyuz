import datetime
from pprint import pprint

import hubspot
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from hubspot.crm.contacts import ApiException, SimplePublicObjectInput
from sentry_sdk import capture_exception

from ..forms import SignUpForm
from ..models import Batch

client = hubspot.Client.create(api_key=settings.HUBSPOT_API_KEY)


@require_GET
def dashboard(request):
    context = {
        "user": request.user,
    }
    batch_query = request.user.batch_set.filter(start_date__gte=datetime.date.today())
    if len(batch_query) > 0:
        batch = batch_query[0]
        context["batch"] = batch
        section_query = request.user.section_set.filter(batch_number=batch.id)
        if len(section_query) > 0:
            context["section"] = section_query[0]

    return render(request, "users/dashboard.html", context)


@require_http_methods(["GET", "POST"])
def signup(request, batch_number, user_hubspot_id):
    batch = Batch.objects.get(number=batch_number)

    if request.method == "GET":

        form = SignUpForm()

        context = {
            "batch_number": batch_number,
            "user_hubspot": user_hubspot_id,
            "form": form,
        }

        return render(request, "users/signup.html", context)

    elif request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid() is False:

            context = {
                "batch_number": batch_number,
                "user_hubspot": user_hubspot_id,
                "form": form,
            }

            return render(request, "users/signup.html", context)

        raw_password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")
        user_github = form.cleaned_data.get("github_username")
        user = get_user_model().objects.create(
            email=email, github_username=user_github, hubspot_id=user_hubspot_id
        )
        user.set_password(raw_password)
        user.save()
        batch.users.add(user)
        section = batch.add_student_to_section(user)

        # send email
        send_email_notification(user, batch, section)

        # set hubspot user data
        update_hubspot(user_hubspot_id)

        login(request, user)

        return redirect("soyuz_app:dashboard")


def update_hubspot(user_hubspot_id):
    properties = {"bootcamp_funnel_status": "basics_apply;basics_register"}

    simple_public_object_input = SimplePublicObjectInput(properties=properties)
    try:
        api_response = client.crm.contacts.basic_api.update(
            contact_id=user_hubspot_id,
            simple_public_object_input=simple_public_object_input,
        )
        pprint(api_response)

    except ApiException as e:
        capture_exception(e)


def send_email_notification(user, batch, section):

    email_text_body = f""" Thanks for signing up for {batch.course.name}
        It starts on {batch.start_date}
        You are in section {section.number}"""

    # TODO: add relevant batch deailts to email
    # send them a confirmation email
    send_mail(
        f"Rocket Academy {batch.course.name} Signup",
        email_text_body,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
    )
