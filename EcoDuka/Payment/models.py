from django.db import models
from django.utils import timezone

from User.models import CustomUser
from Product.models import Product

class Sale(models.Model):
    product = models.ManyToManyField(Product)
    merchant = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="merchant")
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="customer")
    date = models.DateTimeField(timezone.now)
    amount = models.FloatField(default=0)

class PaymentPlan(models.Model):
    period = models.DurationField()
    deposit = models.FloatField(default=0)
    percent = models.FloatField()

class Tracker(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    deposit = models.FloatField(default=0)
    amount_remaining = models.FloatField(default=0)

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(timezone.now)


