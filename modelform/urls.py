from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('employee', views.employee, name="employee"),
    path('office', views.office, name="office"),
    path('city', views.city, name="city"),
    path('job', views.job_list, name="Jobs"),
    path('api/get_jobs/', views.get_jobs),
    path('post/ajax/employee', views.postEmp, name="post_employee"),
    path('get/ajax/name', views.getEmpName, name="get_name"),
    path('post/ajax/office', views.postOff, name="post_office"),
    path('contact', views.contactPost, name="contact"),
    path('check_name', views.checkName, name="check_name"),
    # Bellow are the user creation form
    path('signup', RegistrationView.as_view(), name="signup"),
    path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name="validate_username"),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()), name="validate_email"),
    # Bellow API are the example of crud
    path('crud', views.CrudView.as_view(), name="crud_with_ajax"),
    path('ajax/crud/create/',  views.CreateCrudView.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/',  views.UpdateCrudView.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/',  views.DeleteCrudView.as_view(), name='crud_ajax_delete'),
]