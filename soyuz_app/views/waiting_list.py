from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from soyuz_app.emails.basics_rejection import send_rejection_email

from ..emails.waiting_list_confirmation import send_waiting_list_confirmation
from ..emails.got_off_waitlist import send_got_off_waitlist_notification
from ..models import Batch, Waiting_list, Queue, Section
from ..library.hubspot import Hubspot
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

    waiting_list_position = list(waiting_list.users.all()).index(user)

    waiting_list_count = waiting_list.users.all().count()

    # send email to confirm spot on waitig list
    send_waiting_list_confirmation(user, batch, first_name, waiting_list_count, waiting_list_position)

    context = {
        "waiting_list_position": waiting_list_position,
        "waiting_list_count": waiting_list_count,
        "first_name": first_name,
        "batch": batch
    }

    return context


def check_batch_capacity(batch):
    # check if batch waiting list exists
    try:
        waiting_list = batch.waiting_list
    except Waiting_list.DoesNotExist:
        pass
    else:
        # if waiting list does exist, find out how many empty spaces we have
        # to fill
        slots_to_fill = batch.max_capacity - batch.users.all().count()
        if waiting_list.users.count() > 0:
            # get students to remove from waiting list (order by oldest entry date)
            if slots_to_fill <= waiting_list.users.count():
                students_to_add = list(waiting_list.users.order_by(
                    'queue__entry_date')[0:slots_to_fill])
            else:
                students_to_add = list(waiting_list.users.order_by(
                    'queue__entry_date'))

            # remove selected students from waiting list
            waiting_list.users.remove(*students_to_add)
            # add selected students to batch
            batch.users.add(*students_to_add)

            hubspot_client = Hubspot()
            # update student's funnel status in hubspot
            for student in students_to_add:
                hubspot_client.update_funnel_basics_apply(student.hubspot_id, batch.number)

                # send email notifying students to sign up
                send_got_off_waitlist_notification(student, batch)
                # check if batch has sections
            try:
                sections = Section.objects.filter(batch=batch)
            except Section.DoesNotExist:
                pass
            else:
                for student in students_to_add:
                    # setting count to bigger number than a section will have
                    section_users_count = 1000
                    selected_section = None

                    # looking for the section with the fewest students
                    for section in sections:
                        if section.users.all().count() < section_users_count:
                            section_users_count = section.users.all().count()
                            selected_section = section

                    if selected_section is not None:
                        selected_section.users.add(student)


@staff_member_required
@require_POST
def send_basics_rejection_email(request):
    batch_id = request.POST.get('batch_id')

    batch = Batch.objects.get(id=int(batch_id))
    waiting_list = batch.waiting_list

    course_name = batch.course.name
    batch_number = batch.number
    waiting_list_students = list(waiting_list.users.all())
    print('waiting list students', waiting_list_students)

    for student in waiting_list_students:
        send_rejection_email(student, batch)

    return redirect(
        "soyuz_app:get_sections", course_name=course_name, batch_number=batch_number
    )
