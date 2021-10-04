from django.urls import include, path
from rest_framework import routers

# import the view function from the views file
from . import views

router = routers.DefaultRouter()
router.register(r'batches', views.BatchView, 'batch')

urlpatterns = [
    path('', views.index, name='index'),
    path('registration-success', views.confirm_registration,
         name="registration-success"),
    path('api/', include(router.urls)),
]
