from django.urls import path


from .views import (
    LocationView,
    UserView,
    NotificationsView,
    home,
    contacts,
    store,
    loginuser as login,
)

urlpatterns = [
    path("location/", LocationView.as_view(), name="location"),
    path("location/<int:id>/", LocationView.as_view(), name="location"),
    path("user/", UserView.as_view(), name="user"),
    path("user/<int:id>/", UserView.as_view(), name="user"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
    path("notifications/<int:id>/", NotificationsView.as_view(), name="notification"),
    path("", home, name="home"),
    path("store/", store, name="store"),
    path("contacts/", contacts, name="contacts"),
    path("login/", login, name="login"),
]
