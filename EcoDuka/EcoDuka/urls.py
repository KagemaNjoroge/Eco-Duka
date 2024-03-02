from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("User.urls")),
    path("", include("User.urls")),
    path("", include("Product.urls")),
    path("", include("Payment.urls")),
]
# media files

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
