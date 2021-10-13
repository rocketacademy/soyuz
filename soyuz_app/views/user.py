from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from ..models import Batch
from django.contrib.auth import get_user_model
from ..forms import SignUpForm


class UserView(DetailView):
    template_name = 'users/dashboard.html'

    def get_object(self):
        return self.request.user


def signup(request, batch_number, user_hubspot_id):
    batch = Batch.objects.get(number=batch_number)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user_github = form.cleaned_data.get('github_username')
            print(user_github)
            user = get_user_model().objects.create(
                email=email,
                github_username=user_github, hubspot_id=user_hubspot_id)
            user.set_password(raw_password)
            user.save()
            batch.users.add(user)
            user = authenticate(request, email=user.email,
                                password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('soyuz_app:dashboard')
    else:
        form = SignUpForm()

    context = {
        "title": "Student Registration",
        "batch_number": batch_number,
        "user_hubspot": user_hubspot_id,
        "form": form
    }

    return render(request, 'users/signup.html', context)
