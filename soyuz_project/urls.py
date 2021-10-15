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
from django.contrib import admin
from django.urls import include, path

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
]

if env("DJANGO_ENV") == "development":
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
