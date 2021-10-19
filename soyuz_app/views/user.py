from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView

from ..forms import SignUpForm
from ..models import Batch, Section


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
