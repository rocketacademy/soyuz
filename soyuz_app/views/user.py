import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from ..emails.registration import send_reg_notification
from ..forms import SignUpForm
from ..library.hubspot import Hubspot
from ..models import Batch

days_to_expiration = settings.DAYS_TO_REGISTRATION_EXPIRE
max_capacity = settings.MAX_CAPACITY


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
    # get number of students in batch
    num_students_in_batch = batch.users.count()
    print('number of students', num_students_in_batch)
    # if difference is more than days env var, registration is not allowed
    if difference.days < int(days_to_expiration):
        return render(request, "users/registration-expired.html")
    elif num_students_in_batch > int(max_capacity):
        return render(request, "users/max-capacity.html")
    else:
        if request.method == "GET":

            first_name = request.GET.get("first_name", "")
            last_name = request.GET.get("last_name", "")

            form = SignUpForm(
                initial={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                }
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
            hubspot_client = Hubspot()
            # get batch number
            batch_number = batch.number
            user_hubspot_id = hubspot_client.get_hubspot_id(email)
            hubspot_client.update_hubspot(user_hubspot_id, batch_number)

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
