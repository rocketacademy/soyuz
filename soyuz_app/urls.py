from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

# from rest_framework import routers
from .views import slack, user, web, waiting_list

# router = routers.DefaultRouter()
# router.register(r"batches", rest.BatchView, "batch")

app_name = "soyuz_app"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login"), name="logout"),
    path("dashboard/", login_required(user.dashboard), name="dashboard"),
    path(
        "batch/<batch_id>/email/<email>",
        user.signup,
        name="signup",
    ),
    path("student-admin/batches/", web.get_batches, name="get_batches"),
    path(
        "student-admin/course/<course_name>/batch/<batch_number>",
        web.get_sections,
        name="get_sections",
    ),
    # path("api/", include(router.urls)),
    path("student-admin/switch-sections", web.switch_sections, name="switch_sections"),
    path("student-admin/delete-from-section", web.delete_items, name="switch_sections"),
    path(
        "student-admin/delete-from-batch",
        web.delete_from_batch,
        name="delete_from_batch",
    ),
    path("student-admin/add-to-batch", web.add_to_batch, name="add_to_batch"),
    path("student-admin/add-to-section", web.add_to_section, name="add_to_section"),
    path("student-admin/student-list", web.get_student_list, name="get_student_list"),
    path(
        "student-admin/reassign-sections",
        web.reassign_sections,
        name="reassign_sections",
    ),
    path(
        "student-admin/check-slack-registration",
        web.check_slack_registration,
        name="check_slack_registration",
    ),
    path(
        "student-admin/delete-from-batch-only",
        web.delete_from_batch_only,
        name="delete_from_batch_only",
    ),
    path(
        "student-admin/create-batch-channel",
        web.create_batch_channel,
        name="create_batch_channel",
    ),
    path("student-admin/assign-sections", web.assign_sections, name="assign_sections"),
    path("student-admin/create-channels", web.create_channels, name="create_channels"),
    path('event/hook', slack.event_hook, name='event_hook'),
    path("student-admin/change-batch-capacity", web.change_batch_capacity, name="change_batch_capacity"),
    path('student-admin/course-completed', web.course_completed, name="course_completed"),
    path("student-admin/create-section-channel", web.create_section_channel, name="create_section_channel"),
    path("student-admin/assign-sectionless-students", web.sectionless_assign, name="sectionless_assign"),
    path("student-admin/waiting-list/batch/<batch_id>", waiting_list.get_waiting_list, name="get_waiting_list"),
    path("student-admin/delete-from-waiting-list", waiting_list.delete_from_waiting_list,
         name="delete_from_waiting_list"),
    path("student-admin/join-waiting-list", waiting_list.join_waiting_list, name="join_waiting_list"),
    path("", web.landing_page, name="landing_page"),
]
