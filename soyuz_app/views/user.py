from pprint import pprint

import hubspot
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from hubspot.crm.contacts import ApiException, SimplePublicObjectInput
from sentry_sdk import capture_exception

from ..forms import SignUpForm
from ..models import Batch, Section

client = hubspot.Client.create(api_key=settings.HUBSPOT_API_KEY)


class UserView(DetailView):
    template_name = "users/dashboard.html"

    def get_object(self):
        return self.request.user


def signup(request, batch_number, user_hubspot_id):
    batch = Batch.objects.get(number=batch_number)
    max_students = 4

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user_github = form.cleaned_data.get("github_username")
            user = get_user_model().objects.create(
                email=email, github_username=user_github, hubspot_id=user_hubspot_id
            )
            user.set_password(raw_password)
            user.save()
            batch.users.add(user)

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

            sections = Section.objects.all().order_by("-number")
            if sections.count() > 0:
                if sections[0].users.count() <= max_students:
                    sections[0].users.add(user)
                else:
                    new_section = Section.objects.create(
                        number=sections.count() + 1, batch_id=batch
                    )
                    new_section.users.add(user)
            else:
                new_section = Section.objects.create(number=1, batch_id=batch)
                new_section.users.add(user)

            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:

                # TODO: add relevant batch deailts to email
                # send them a confirmation email
                send_mail(
                    "Rocket Basics Signup",
                    "Thanks for signing up for basics.",
                    "Rocket Academy <hello@rocketacademy.co>",
                    [user.email],
                )

                login(request, user)
            else:
                print("user is not authenticated")
            return redirect("soyuz_app:dashboard")
    else:
        form = SignUpForm()

    context = {
        "title": "Student Registration",
        "batch_number": batch_number,
        "user_hubspot": user_hubspot_id,
        "form": form,
    }

    return render(request, "users/signup.html", context)
