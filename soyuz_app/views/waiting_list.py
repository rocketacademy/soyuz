from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from ..models import Batch, Waiting_list, Queue
from django.shortcuts import redirect, render


@staff_member_required
@require_GET
def get_waiting_list(request, batch_id):

    batch = Batch.objects.get(id=batch_id)

    try:
        batch_waiting_list = batch.waiting_list

    except Waiting_list.DoesNotExist:
        batch_waiting_list = None
        waiting_list_queue = None

    else:
        waiting_list_queue = list(Queue.objects.filter(waiting_list=batch_waiting_list).order_by("entry_date"))

    context = {
        "batch": batch,
        "waiting_list": batch_waiting_list,
        "waiting_list_queue": waiting_list_queue
    }

    return render(request, "waiting-list.html", context)


@staff_member_required
@require_POST
def delete_from_waiting_list(request):
    batch_id = int(request.POST.get('batch_id'))
    students_to_delete = request.POST.getlist('student_id')
    batch = Batch.objects.get(id=batch_id)

    waiting_list = batch.waiting_list

    for student_id in students_to_delete:
        waiting_list.users.remove(int(student_id))

    return redirect('soyuz_app:get_waiting_list', batch_id=batch_id)


def create_or_join_waiting_list(batch, user, first_name, datetime):
    try:
        waiting_list = batch.waiting_list

    except Waiting_list.DoesNotExist:
        waiting_list = Waiting_list.objects.create(
            batch=batch
        )

    waiting_list.users.add(user, through_defaults={'entry_date': datetime.date.today()})

    waiting_list_count = waiting_list.users.all().count()

    context = {
        "waiting_list_count": waiting_list_count,
        "first_name": first_name,
        "batch": batch
    }

    return context
