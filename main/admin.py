from django.contrib import admin
from .models import UserContact, Tracker, Alert
# Register your models here.

admin.site.register(UserContact)
admin.site.register(Tracker)
admin.site.register(Alert)

