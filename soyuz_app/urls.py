from django.urls import include, path
from rest_framework import routers

# import the view function from the views file
from . import views

router = routers.DefaultRouter()
router.register(r'batches', views.BatchView, 'batch')

urlpatterns = [
    path('batch/<batch_number>/hubspot_id/<user_hubspot_id>',
         views.student_registration, name='student_registration'),
    path('student-admin/batches/', views.get_batches, name='get_batches'),
    path('student-admin/batch/<batch_id>',
         views.get_sections, name='get_sections'),
    path('', views.index, name='index'),
    path('registration-success', views.confirm_registration,
         name="registration-success"),
    path('api/', include(router.urls)),
]
