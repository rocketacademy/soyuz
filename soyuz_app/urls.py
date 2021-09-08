from django.urls import path

# import the view function from the views file
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
