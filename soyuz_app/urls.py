from django.urls import include, path
from rest_framework import routers
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# import the view function from the views file
from .views import UserView, signup
from . import views

router = routers.DefaultRouter()
router.register(r'batches', views.BatchView, 'batch')

app_name = 'soyuz_app'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('dashboard/',  login_required(UserView.as_view()), name='dashboard'),
    path('batch/<batch_number>/hubspot_id/<user_hubspot_id>',
         signup, name='signup'),
    #     path('batch/<batch_number>/hubspot_id/<user_hubspot_id>',
    #          views.student_registration, name='student_registration'),
    path('student-admin/batches/', views.get_batches, name='get_batches'),
    path('student-admin/batch/<batch_id>',
         views.get_sections, name='get_sections'),
    path('registration-success', views.confirm_registration,
         name="registration-success"),
    path('api/', include(router.urls)),
]
