from django.contrib import admin

# Register your models here.
from .models import Patient,Therapist

from django.contrib import admin


admin.site.register(Patient)
admin.site.register(Therapist)