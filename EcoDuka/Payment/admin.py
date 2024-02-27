from django.contrib import admin
from .models import Payment, PaymentPlan, Tracker, Sale

admin.site.register(Payment)
admin.site.register(PaymentPlan)
admin.site.register(Tracker)
admin.site.register(Sale)
