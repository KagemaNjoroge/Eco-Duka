from django.urls import path


from .views import LocationView, UserView, NotificationsView

urlpatterns = [
    path("location/", LocationView.as_view(), name="location"),
    path("location/<int:id>/", LocationView.as_view(), name="location"),
    path("user/", UserView.as_view(), name="user"),
    path("user/<int:id>/", UserView.as_view(), name="user"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
    path("notifications/<int:id>/", NotificationsView.as_view(), name="notification"),
]
