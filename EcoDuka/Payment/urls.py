from django.urls import path
from .views import PaymentPlanView, SalesView, PaymentView

urlpatterns = [
    path("sales/", SalesView.as_view(), name="sales"),
    path("sales/<int:id>/", SalesView.as_view(), name="sale"),
    path("payment-plans/", PaymentPlanView.as_view(), name="payment-plans"),
    path("payment-plans/<int:id>/", PaymentPlanView.as_view(), name="payment-plan"),
    path("payments/", PaymentView.as_view(), name="payments"),
    path("payments/<int:id>/", PaymentView.as_view(), name="payment"),
]
