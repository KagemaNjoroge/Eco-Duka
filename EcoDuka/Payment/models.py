from django.db import models
from django.utils import timezone

from User.models import CustomUser
from Product.models import Product


class Sale(models.Model):
    product = models.ManyToManyField(Product)
    merchant = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="merchant"
    )
    customer = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="customer"
    )
    date = models.DateTimeField(timezone.now)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product} sold to {self.customer} by {self.merchant}"

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


class PaymentPlan(models.Model):
    period = models.DurationField()
    deposit = models.FloatField(default=0)
    percent = models.FloatField()

    def __str__(self):
        return f"{self.period} plan with {self.percent} interest"

    class Meta:
        verbose_name = "Payment Plan"
        verbose_name_plural = "Payment Plans"


class Tracker(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    deposit = models.FloatField(default=0)
    amount_remaining = models.FloatField(default=0)

    def __str__(self):
        return f"{self.sale} with {self.amount_remaining} remaining"

    class Meta:
        verbose_name = "Tracker"
        verbose_name_plural = "Trackers"


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(timezone.now)

    def __str__(self):
        return f"{self.user} paid {self.amount}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
