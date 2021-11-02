from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from rest_framework import routers

from . import views
from .views import (
    dashboard,
    delete_items,
    get_batches,
    get_sections,
    signup,
    switch_sections,
)

router = routers.DefaultRouter()
router.register(r"batches", views.BatchView, "batch")

app_name = "soyuz_app"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login"), name="logout"),
    path("dashboard/", login_required(dashboard), name="dashboard"),
    path(
        "batch/<batch_id>/email/<email>",
        signup,
        name="signup",
    ),
    path("student-admin/batches/", get_batches, name="get_batches"),
    path("student-admin/batch/<batch_id>", get_sections, name="get_sections"),
    path("api/", include(router.urls)),
    path("student-admin/switch-sections", switch_sections, name="switch_sections"),
    path("student-admin/delete-from-section", delete_items, name="switch_sections"),
]
