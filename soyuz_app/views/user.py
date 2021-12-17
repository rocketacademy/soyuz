import datetime
from pprint import pprint

import hubspot
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from hubspot.crm.contacts import (
    ApiException,
    Filter,
    FilterGroup,
    PublicObjectSearchRequest,
    SimplePublicObjectInput,
)
from sentry_sdk import capture_exception

from ..emails.registration import send_reg_notification
from ..forms import SignUpForm
from ..models import Batch

client = hubspot.Client.create(api_key=settings.HUBSPOT_API_KEY)
days_to_expiration = settings.DAYS_TO_REGISTRATION_EXPIRE


@require_GET
def dashboard(request):
    context = {
        "user": request.user,
    }
    batch_query = request.user.batch_set.filter(
        start_date__gte=datetime.date.today()
    ).order_by("start_date")

    batches = []
    if len(batch_query) > 0:
        for batch in batch_query:
            user_batch = {"batch": batch}
            results = batch.section_set.filter(users=request.user)
            if len(results) > 0:
                user_batch["section"] = results[0]
            batches.append(user_batch)
        context["batches"] = batches

        # pprint(batches[0]["section"].number)
    return render(request, "users/dashboard.html", context)


@require_http_methods(["GET", "POST"])
def signup(request, batch_id, email):

    batch = Batch.objects.get(pk=batch_id)
    # get batch start date
    start_date = batch.start_date
    # get today's date
    today = datetime.date.today()
    # check difference
    difference = start_date - today
    # if difference is more than days env var, registration is not allowed
    if difference.days < int(days_to_expiration):
        return render(request, "users/registration-expired.html")
    else:
        if request.method == "GET":

            first_name = request.GET.get("first_name", "")
            last_name = request.GET.get("last_name", "")

            form = SignUpForm(
                initial={"email": email, "first_name": first_name, "last_name": last_name}
            )

            context = {
                "email": email,
                "batch": batch,
                "form": form,
            }

            return render(request, "users/signup.html", context)

        elif request.method == "POST":

            form = SignUpForm(request.POST)

            if form.is_valid() is False:

                context = {
                    "email": email,
                    "form": form,
                }

                return render(request, "users/signup.html", context)

            raw_password = form.cleaned_data.get("password1")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")

            # set hubspot user data
            user_hubspot_id = get_hubspot_id(email)
            update_hubspot(user_hubspot_id)

            user = get_user_model().objects.create(
                email=email,
                hubspot_id=user_hubspot_id,
                first_name=first_name,
                last_name=last_name,
            )

            user.set_password(raw_password)
            user.save()

            batch.users.add(user)
            # section = batch.add_student_to_section(user)

            # send email
            send_reg_notification(user, batch)

            login(request, user)

            return redirect("soyuz_app:dashboard")


def get_hubspot_id(email):
    try:
        # from: https://github.com/HubSpot/hubspot-api-python/issues/49#issuecomment-811911302
        email_filter = Filter(property_name="email", operator="EQ", value=email)

        first_group = FilterGroup(filters=[email_filter])

        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[first_group]
        )

        api_response = client.crm.contacts.search_api.do_search(
            public_object_search_request=public_object_search_request
        )

        result = api_response.to_dict()

        if (
            result["total"] == 0
            or "results" not in result
            or len(result["results"]) == 0
        ):
            raise ValueError("no hubspot user email")

        return result["results"][0]["properties"]["hs_object_id"]
    except ApiException as e:
        capture_exception(e)
        raise ValueError("error getting hubspot user email")


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
        raise ValueError("error updating hubspot")
