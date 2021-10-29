from django.contrib.auth import get_user_model
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


def get_sections(request, batch_number):
    batch = Batch.objects.get(number=batch_number)
    sections = Section.objects.filter(batch=batch)
    users = batch.users.all()
    print(users)
    section_array = []
    for section in sections:
        section_obj = {}
        section_obj["number"] = section.number
        section_users = section.users.all()
        section_obj["users"] = section_users
        section_array.append(section_obj)

    if "delete_items" in request.POST:
        # Fetch user id and section name of user we want to remove from a section
        user_to_delete = request.POST.get("delete_items")
        user_to_delete = user_to_delete.split("/")
        # section that user is in
        selected_section = Section.objects.get(number=int(user_to_delete[0]))
        # user that we want to delete
        user = get_user_model().objects.get(id=int(user_to_delete[1]))
        selected_section.users.remove(user)

        # fetch destinaton section number and user id
    elif "batch_sections" in request.POST:
        section_to_move = request.POST["batch_sections"]
        section_to_move = section_to_move.split("/")
        # user that we want to move
        selected_user = get_user_model().objects.get(id=int(section_to_move[1]))
        # user's original section
        user_section = Section.objects.get(users__id=int(section_to_move[1]))
        # user's destination section
        destination_section = Section.objects.get(number=int(section_to_move[0]))
        user_section.users.remove(selected_user)
        destination_section.users.add(selected_user)

    context = {
        "title": "List of Sections",
        "batch": batch,
        "sections": section_array,
    }

    return render(request, "section-page.html", context)
