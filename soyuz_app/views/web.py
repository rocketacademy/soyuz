from django.shortcuts import render, redirect

from django.http import HttpResponse
from ..models import Batch, Section, Course
from accounts.forms import RegistrationForm
from ..forms import AddBatchForm


def index(request):

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
        "form": registration_form
    }
    return render(request, "index.html", context)


def confirm_registration(request):
    return render(request, 'registration_success.html')


def get_batches(request):
    batches = Batch.objects.all()
    print(batches)

    if request.method == 'GET':
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {
        "title": "List of Batches",
        "batches": batches,
        "form": add_batch_form
    }
    return render(request, 'batch-page.html', context)


def get_sections(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    sections = Section.objects.filter(batch_id=batch_id)

    section_array = []
    for section in sections:
        section_obj = {}
        section_obj['number'] = section.number
        section_users = section.users.all()
        section_obj['users'] = section_users
        section_array.append(section_obj)

    context = {
        "title": "List of Sections",
        "batch": batch,
        "sections": section_array
    }

    return render(request, 'section-page.html', context)


def student_registration(request, batch_number, user_hubspot_id):
    batch = Batch.objects.get(number=batch_number)
    if request.method == 'GET':
        registration_form = RegistrationForm()
    else:
        registration_form = RegistrationForm(request.POST)
        # if registration_form.is_valid():
        #     user_github = registration_form.cleaned_data['github_username']
        #     print(user_github)
        #     user = User.objects.create(
        #         github_username=user_github, hubspot_id=user_hubspot_id)
        #     batch.users.add(user)
        redirect('registration-success')

    context = {
        "title": "Student Registration",
        "batch_number": batch_number,
        "user_hubspot": user_hubspot_id,
        "form": registration_form
    }
    return render(request, 'student-registration.html', context)
