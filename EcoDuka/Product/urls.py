from django.urls import path

from EcoDuka.Product.views import ProductView

urlpatterns = [
    path("product/", ProductView.as_view(), name="product"),
    path("product/<int:id>/", ProductView.as_view(), name="product"),
]
