from django.urls import path

from .views import ProductView, CategoryView, search

urlpatterns = [
    path("product/", ProductView.as_view(), name="product"),
    path("product/<int:id>/", ProductView.as_view(), name="product"),
    path("category/", CategoryView.as_view(), name="category"),
    path("category/<int:id>/", CategoryView.as_view(), name="category"),
    path("search/", search, name="search"),
]
