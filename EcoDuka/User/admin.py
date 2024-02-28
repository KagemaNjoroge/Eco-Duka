from django.contrib import admin
from .models import CustomUser, Location, Notification


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "user_type",
        "location",
        "time_created",
    ]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["county", "sub_county", "ward"]


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "date", "read"]
