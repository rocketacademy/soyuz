from django.shortcuts import render

from ..forms import AddBatchForm
from ..models import Batch, Section


def confirm_registration(request):
    return render(request, "registration_success.html")


def get_batches(request):
    batches = Batch.objects.all()
    print(batches)

    if request.method == "GET":
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {"title": "List of Batches", "batches": batches, "form": add_batch_form}
    return render(request, "batch-page.html", context)


def get_sections(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    sections = Section.objects.filter(batch_id=batch_id)
    users = batch.users.all()
    print(users)
    section_array = []
    for section in sections:
        section_obj = {}
        section_obj["number"] = section.number
        section_users = section.users.all()
        section_obj["users"] = section_users
        section_array.append(section_obj)

    context = {
        "title": "List of Sections",
        "batch": batch,
        "sections": section_array,
    }

    return render(request, "section-page.html", context)
