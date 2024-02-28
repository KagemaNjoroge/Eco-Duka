from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("User.urls")),
    path("", include("User.urls")),
    path("", include("Product.urls")),
    path("", include("Payment.urls")),
]
