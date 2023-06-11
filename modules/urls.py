# from .views import *

from django.urls import path
from . import views
from modules.views import * 


urlpatterns = [
    path('', views.home, name='home'),
    path('mycalendly/(?P<user>\d+)/$', views.mycalendly, name='mycalendly'),
    path('mycalendlyregister/(?P<user>\d+)/$', views.mycalendlyregister, name='mycalendlyregister'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dash/(?P<user>.*)/$', views.dash, name='dash'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),

]