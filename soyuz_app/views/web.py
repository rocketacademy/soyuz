from django.shortcuts import render, redirect

from django.http import HttpResponse
from ..models import Batch, Section, User
from ..forms import RegistrationForm


def index(request):
    batches = Batch.objects.all()

    if request.method == 'GET':
        registration_form = RegistrationForm()
    else:
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            print(user)
            return redirect('registration-success')

    context = {
        "title": "index",
        "batches": batches,
        "form": registration_form
    }
    return render(request, "index.html", context)


def confirm_registration(request):
    return render(request, 'registration_success.html')
