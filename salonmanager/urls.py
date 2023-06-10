from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_login, name='manager_login'),
    path('manager_signup/', views.manager_signup, name='manager_signup'),
    path('manager_dashboard/',views.manager_dashboard,name='manager_dashboard'),
    path('appointment_booking',views.appointment_booking,name='appointment_booking'),
    path('save_appointment', views.save_appointment, name='save_appointment')
]
