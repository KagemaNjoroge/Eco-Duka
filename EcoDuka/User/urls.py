from django.urls import path


from .views import LocationView

urlpatterns = [
    path("location/", LocationView.as_view(), name="location"),
    path("location/<int:id>/", LocationView.as_view(), name="location"),
]
