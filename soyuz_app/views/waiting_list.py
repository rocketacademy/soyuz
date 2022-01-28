from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from ..models import Batch, Waiting_list
from django.shortcuts import redirect, render


@staff_member_required
@require_GET
def get_waiting_list(request, batch_id):

    batch = Batch.objects.get(id=batch_id)

    try:
        batch_waiting_list = batch.waiting_list

    except Waiting_list.DoesNotExist:
        batch_waiting_list = None
        waiting_list_students = None

    else:
        if batch_waiting_list is not None:
            waiting_list_students = get_user_model().objects.filter(waiting_list=batch_waiting_list)

    context = {
        "waiting_list_students": waiting_list_students
    }

    return render(request, "waiting-list.html", context)
