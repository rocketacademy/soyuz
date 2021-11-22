"""soyuz_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

import environ
from django.conf.urls import handler404, handler500  # , handler403, handler400
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from soyuz_app.views.error import custom_error_404, custom_error_500

# assign the custom error handling views
handler404 = custom_error_404  # noqa: F811
handler500 = custom_error_500  # noqa: F811

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "soyuz"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("soyuz_app.urls")),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password-reset.html"),
        name="password_reset_email",
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password-reset-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
]

if env("DJANGO_ENV") == "development":
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
