from django.urls import path
from .views import *

urlpatterns = [
    path('',log_in,name='log_in'),
    path('index/',index,name='index'),
    path('register/',register,name='register'),
    path('log_out/',log_out,name='log_out'),
    path('change_password/',change_password,name='change_password'),
]
