from django.contrib import admin
from .models import CustomUser, Location, Notification

admin.site.register(CustomUser)
admin.site.register(Location)
admin.site.register(Notification)
