import datetime

from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from ..forms import SignUpForm
from ..models import Batch, Section


def dashboard(request):
    context = {
        "user": request.user,
    }
    batch_query = request.user.batch_set.filter(start_date__gte=datetime.date.today())
    if len(batch_query) > 0:
        batch = batch_query[0]
        context["batch"] = batch
        section_query = request.user.section_set.filter(batch_id=batch.id)
        if len(section_query) > 0:
            context["section"] = section_query[0]

    return render(request, "users/dashboard.html", context)


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
            sections = Section.objects.all().order_by("-number")
            if sections.count() > 0:
                if sections[0].users.count() <= max_students:
                    section = sections[0]
                    section.users.add(user)
                else:
                    section = Section.objects.create(
                        number=sections.count() + 1, batch_id=batch
                    )
                    section.users.add(user)
            else:
                section = Section.objects.create(number=1, batch_id=batch)
                section.users.add(user)

            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:

                send_email_notification(user, batch, section)

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


def send_email_notification(user, batch, section):

    email_text_body = f""" Thanks for signing up for {batch.course_id.name}
        It starts on {batch.start_date}
        You are in section {section.number}"""

    # TODO: add relevant batch deailts to email
    # send them a confirmation email
    send_mail(
        f"Rocket Academy {batch.course_id.name} Signup",
        email_text_body,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
    )
