import math
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from ..forms import AddBatchForm
from ..models import Batch, Section


@require_http_methods(["GET", "POST"])
def get_batches(request):
    batches = Batch.objects.all()

    if request.method == "GET":
        add_batch_form = AddBatchForm()
    else:
        add_batch_form = AddBatchForm(request.POST)
        if add_batch_form.is_valid():
            new_batch = add_batch_form.save()
            print(new_batch)

    context = {"title": "List of Batches", "batches": batches, "form": add_batch_form}
    return render(request, "batch-page.html", context)


@require_POST
def add_to_batch(request):
    batch_id = int(request.POST.get('batch_id'))
    user_id = int(request.POST.get('user_id'))

    destination_batch = Batch.objects.get(id=batch_id)
    user = get_user_model().objects.get(id=user_id)

    destination_batch.users.add(user)

    return redirect("soyuz_app:get_batches")


@require_GET
def get_student_list(request):
    # getting users that are in a batch
    users = get_user_model().objects.filter(batch__isnull=False, is_superuser=False, is_staff=False)

    # getting users who do not belong in any batch
    users_no_batch = get_user_model().objects.filter(batch__isnull=True, is_superuser=False, is_staff=False)

    # getting all batches
    batches = Batch.objects.all()
    context = {"title": "Student List", "users": users, "users_no_batch": users_no_batch, "batches": batches}

    return render(request, 'student-list.html', context)


@require_GET
def get_sections(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    users = get_user_model().objects.filter(batch=batch, section__isnull=True, is_superuser=False, is_staff=False)
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
        "users": users
    }

    return render(request, "section-page.html", context)


@require_POST
def delete_from_batch(request):
    user_id = int(request.POST.get('user_id'))
    section_id = int(request.POST.get('section_id'))
    batch_id = int(request.POST.get('batch_id'))

    print(user_id)
    print(section_id)
    print(batch_id)
    user = get_user_model().objects.get(id=user_id)
    batch = Batch.objects.get(id=batch_id)
    section = Section.objects.get(id=section_id)

    section.users.remove(user)
    batch.users.remove(user)

    return redirect("soyuz_app:get_sections", batch_id=batch_id)


@require_POST
def reassign_sections(request):
    # data from form
    number_per_section = int(request.POST.get('number_per_section'))
    batch_id = int(request.POST.get('batch_id'))

    # get all users in batch
    batch = Batch.objects.get(id=batch_id)
    batch_users = list(get_user_model().objects.filter(batch=batch))
    print(batch_users)
    # get number of users in batch
    number_of_users = len(batch_users)
    print(number_of_users)

    # delete batch sections
    Section.objects.filter(batch=batch).delete()

    number_of_sections = math.ceil(number_of_users / number_per_section)

    for i in range(number_of_sections):
        # create new section
        new_section = Section.objects.create(number=i + 1, batch=batch)
        for j in range(number_per_section):
            # add users to new sections
            if len(batch_users) > 0:
                new_user = batch_users.pop()
                new_section.users.add(new_user)

    return redirect("soyuz_app:get_sections", batch_id=batch_id)


@require_POST
def add_to_section(request):
    user_id = int(request.POST.get('user_id'))
    section_id = int(request.POST.get('section_id'))
    destination_section = Section.objects.get(id=section_id)
    batch_id = int(request.POST.get('batch_id'))

    user = get_user_model().objects.get(id=user_id)
    destination_section.users.add(user)

    return redirect("soyuz_app:get_sections", batch_id=batch_id)


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
