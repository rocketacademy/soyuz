from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from ..forms import AddBatchForm
from ..models import Batch, Section


@require_http_methods(["GET", "POST"])
def get_batches(request):
    batches = Batch.objects.all()
    print(batches)

    # getting all users who do not belong in any batch
    users = get_user_model().objects.filter(batch__isnull=True, is_superuser=False, is_staff=False)
    print(users)

    if request.method == "GET":
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {"title": "List of Batches", "batches": batches, "form": add_batch_form, 'users': users}
    return render(request, "batch-page.html", context)


@require_POST
def add_to_batch(request):
    batch_id = request.POST.get('batch_id')
    user_id = request.POST.get('user_id')

    destination_batch = Batch.objects.get(id=batch_id)
    user = get_user_model().objects.get(id=user_id)

    destination_batch.users.add(user)

    return redirect("soyuz_app:get_batches")


@require_GET
def get_sections(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    sections = batch.section_set.all()
    section_array = []
    for section in sections:
        section_obj = {}
        section_obj["id"] = section.id
        section_obj["number"] = section.number
        section_users = section.users.all()
        section_obj["users"] = section_users
        section_array.append(section_obj)

    context = {
        "batch": batch,
        "sections": section_array,
    }

    return render(request, "section-page.html", context)


@require_POST
def delete_items(request):
    # Fetch user id and section name of user we want to remove from a section
    user_to_delete = request.POST.get("user_id")
    user_section = request.POST.get("section_id")
    batch_id = request.POST.get("batch_id")

    # section that user is in
    selected_section = Section.objects.get(id=int(user_section))
    # # user that we want to delete
    user = get_user_model().objects.get(id=int(user_to_delete))
    selected_section.users.remove(user)

    return redirect("soyuz_app:get_sections", batch_id=batch_id)


@require_POST
# fetch destinaton section number and user id
def switch_sections(request):
    section_destination = request.POST.get("section_number")
    user_to_move = request.POST.get("user_id")
    batch_id = request.POST.get("batch_id")

    # user that we want to move
    selected_user = get_user_model().objects.get(id=int(user_to_move))
    # # user's original section
    user_section = Section.objects.get(users__id=int(user_to_move))
    # # user's destination section
    destination_section = Section.objects.get(id=int(section_destination))
    user_section.users.remove(selected_user)
    destination_section.users.add(selected_user)

    return redirect("soyuz_app:get_sections", batch_id=batch_id)
