from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from modules.urls import *

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('modules.urls')),
    path('verification/', include('verify_email.urls')),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)