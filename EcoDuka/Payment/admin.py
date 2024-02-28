from django.contrib import admin
from .models import Payment, PaymentPlan, Tracker, Sale


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "date"]


class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ["period", "deposit", "percent"]


class TrackerAdmin(admin.ModelAdmin):
    list_display = ["sale", "deposit", "amount_remaining"]


class SaleAdmin(admin.ModelAdmin):
    list_display = ["merchant", "customer", "date", "amount"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentPlan, PaymentPlanAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Sale, SaleAdmin)
