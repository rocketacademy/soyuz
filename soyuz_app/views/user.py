import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from ..emails.registration import send_reg_notification
from ..forms import SignUpForm
from ..library.hubspot import Hubspot
from ..models import Batch
from .waiting_list import create_or_join_waiting_list

# from env vars
days_to_expiration = settings.DAYS_TO_REGISTRATION_EXPIRE
batch_max_capacity = settings.BATCH_MAX_CAPACITY


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

    return render(request, "users/dashboard.html", context)


# depending on whether the number of students in a batch exceeds batch capacity,
# a different page is displayed
def template_to_display(num_students_in_batch, batch_capacity):
    if num_students_in_batch >= int(batch_capacity):
        template = "users/max-capacity.html"
    else:
        template = "users/signup.html"

    return template


@require_http_methods(["GET", "POST"])
def signup(request, batch_id, email):
    batch = Batch.objects.get(pk=batch_id)

    # get batch's max capacity
    if batch.max_capacity is None:
        # from env var
        batch_capacity = batch_max_capacity
    else:
        # from database
        batch_capacity = batch.max_capacity

    # get batch start date
    start_date = batch.start_date
    # get today's date
    today = datetime.date.today()
    # check difference
    difference = start_date - today
    # get number of students in batch
    num_students_in_batch = batch.users.count()

    # set hubspot client
    hubspot_client = Hubspot()

    batch_number = batch.number
    # check to see if user already exists in database
    try:
        user = get_user_model().objects.get(email=email)

    # if user does not exist, render signup form
    except get_user_model().DoesNotExist:
        if request.method == 'GET':
            first_name = request.GET.get("first_name", "")
            last_name = request.GET.get("last_name", "")

            # if difference is more than days env var, registration is not allowed
            if difference.days < int(days_to_expiration):
                return render(request, "users/registration-expired.html")

            else:
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

                template = template_to_display(num_students_in_batch, batch_capacity)

                return render(request, template, context)

        elif request.method == "POST":
            form = SignUpForm(request.POST)

            if form.is_valid() is False:

                context = {
                    "email": email,
                    "form": form,
                }

                template = template_to_display(num_students_in_batch, batch_capacity)
                return render(request, template, context)

            raw_password = form.cleaned_data.get("password1")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")

            user_hubspot_id = hubspot_client.get_hubspot_id(email)

            user = get_user_model().objects.create(
                email=email,
                hubspot_id=user_hubspot_id,
                first_name=first_name,
                last_name=last_name,
            )

            user.set_password(raw_password)
            user.save()

            # whether or not the batch max capacity is exceeded determines if
            # the student is added to the batch or batch waiting list
            if num_students_in_batch >= int(batch_capacity):
                context = create_or_join_waiting_list(batch, user, first_name, datetime)

                return render(request, "users/waiting-list-confirmation.html", context)

            else:
                hubspot_client.update_funnel_basics_apply(user_hubspot_id, batch_number)
                batch.users.add(user)

                # send emails
                # send_reg_notification(user, batch)

                login(request, user)

                return redirect("soyuz_app:dashboard")

    else:
        # whether or not the batch max capacity is exceeded determines if
        # the student is added to the batch or batch waiting list
        if num_students_in_batch >= int(batch_capacity):
            context = create_or_join_waiting_list(batch, user, first_name, datetime)

            return render(request, "users/waiting-list-confirmation.html", context)

        else:
            user_hubspot_id = hubspot_client.get_hubspot_id(email)
            hubspot_client.update_funnel_basics_apply(user_hubspot_id, batch_number)
            batch.users.add(user)

            # send emails
            send_reg_notification(user, batch)

            login(request, user)

            return redirect("soyuz_app:dashboard")
