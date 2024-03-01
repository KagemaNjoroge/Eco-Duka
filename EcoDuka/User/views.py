import json
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from .models import CustomUser, Location, Notification
from Product.models import Product, Category
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "index.html")


def contacts(request):
    return render(request, "contacts.html")


def store(request: HttpRequest) -> HttpResponse:
    # all products
    products = Product.objects.all()
    # all categories
    categories = Category.objects.all()

    return render(
        request, "store.html", {"products": products, "categories": categories}
    )


@method_decorator(csrf_exempt, name="dispatch")
class LocationView(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        if id:
            location = get_object_or_404(Location, id=id)
            return JsonResponse(
                location.to_json(),
            )
        else:
            locations = Location.objects.all()
            return JsonResponse(
                {"locations": [location.to_json() for location in locations]}
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        location = Location.objects.create(
            county=data["county"], sub_county=data["sub_county"], ward=data["ward"]
        )
        location.save()
        return JsonResponse(location.to_json())

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        location = get_object_or_404(Location, id=id)
        location.county = data["county"]
        location.sub_county = data["sub_county"]
        location.ward = data["ward"]
        location.save()
        return JsonResponse(location.to_json())

    def delete(self, request: HttpRequest, id) -> JsonResponse:
        location = get_object_or_404(Location, id=id)
        try:
            location.delete()
            return JsonResponse({"message": "Location deleted successfully."})
        except Exception as e:
            return JsonResponse(
                {"message": "Location deletion failed.", "error": str(e)}
            )


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        if id:
            user = get_object_or_404(CustomUser, id=id)
            return JsonResponse(
                user.to_json(),
            )
        else:
            users = CustomUser.objects.all()
            return JsonResponse({"users": [user.to_json() for user in users]})

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        user = CustomUser.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            location=Location.objects.get(id=data["location"]),
        )
        user.save()
        return JsonResponse(user.to_json())

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        user = get_object_or_404(CustomUser, id=id)
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.phone_number = data["phone_number"]
        user.location = Location.objects.get(id=data["location"])
        user.save()
        return JsonResponse(user.to_json())

    def delete(self, request: HttpRequest, id) -> JsonResponse:
        user = get_object_or_404(CustomUser, id=id)
        try:
            user.delete()
            return JsonResponse({"message": "User deleted successfully."})
        except Exception as e:
            return JsonResponse({"message": "User deletion failed.", "error": str(e)})


@method_decorator(csrf_exempt, name="dispatch")
class NotificationsView(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        if id:
            notification = get_object_or_404(Notification, id=id)
            return JsonResponse(
                notification.to_json(),
            )
        else:
            notifications = Notification.objects.filter(user=request.user)

            return JsonResponse(
                {
                    "notifications": [
                        notification.to_json() for notification in notifications
                    ]
                }
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        notification = Notification.objects.create(
            user=request.user, content=data["content"]
        )
        notification.save()
        return JsonResponse(notification.to_json())

    def delete(self, request: HttpRequest, id) -> JsonResponse:
        notification = get_object_or_404(Notification, id=id)
        try:
            notification.delete()
            return JsonResponse({"message": "Notification deleted successfully."})
        except Exception as e:
            return JsonResponse(
                {"message": "Notification deletion failed.", "error": str(e)}
            )

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        notification = get_object_or_404(Notification, id=id)
        notification.read = data["read"]
        notification.save()
        return JsonResponse(notification.to_json())
