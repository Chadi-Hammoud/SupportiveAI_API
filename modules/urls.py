
# from .views import *

from django.urls import path
from . import views
from modules.views import *
from . import api
from modules.api import *

urlpatterns = [
    path('', views.home, name='home'),
    path('checkemail', views.checkemail, name='checkemail'),
    path('mycalendly/(?P<user>\d+)/$', views.mycalendly, name='mycalendly'),
    path('drboard/(?P<user>\d+)/$', views.drboard, name='drboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',views.logout_view,name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('dash/(?P<user>.*)/$', views.dash, name='dash'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('forget/',views.forget,name="forget"),
    path('changepass/(?P<user>\d+)/$', views.changepass, name='changepass'),
    path('codeVerif/(?P<user>\d+)/<hashed_number>', views.codeVerif, name='codeVerif'),
    path('profilep/',views.profilep,name="profilep"),
    path('profiled/',views.profiled,name="profiled"),
    path('login-api/', LoginViewApi.as_view(), name='login-api'),
    # path('forget-api/',api.forgetApi,name="forget"),
    path('register-api/', RegisterViewApi.as_view(), name='register-api'),
    path('searchdr/',views.searchdr,name="searchdr"),


]