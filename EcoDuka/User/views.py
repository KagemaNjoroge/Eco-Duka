import json
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpRequest, JsonResponse
from .models import Location
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class LocationView(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        if id:
            location = get_object_or_404(Location, id=id)
            return JsonResponse(
                {
                    "county": location.county,
                    "sub_county": location.sub_county,
                    "ward": location.ward,
                    "id": location.id,
                }
            )
        else:
            locations = Location.objects.all()
            return JsonResponse(
                {
                    "locations": [
                        {
                            "county": location.county,
                            "sub_county": location.sub_county,
                            "ward": location.ward,
                            "id": location.id,
                        }
                        for location in locations
                    ]
                }
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        location = Location.objects.create(
            county=data["county"], sub_county=data["sub_county"], ward=data["ward"]
        )
        location.save()
        return JsonResponse(
            {
                "county": location.county,
                "sub_county": location.sub_county,
                "ward": location.ward,
                "id": location.id,
            }
        )

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body.decode("utf-8")
        data = json.loads(data)
        location = get_object_or_404(Location, id=id)
        location.county = data["county"]
        location.sub_county = data["sub_county"]
        location.ward = data["ward"]
        location.save()
        return JsonResponse(
            {
                "county": location.county,
                "sub_county": location.sub_county,
                "ward": location.ward,
                "id": location.id,
            }
        )

    def delete(self, request: HttpRequest, id) -> JsonResponse:
        location = get_object_or_404(Location, id=id)
        try:
            location.delete()
            return JsonResponse({"message": "Location deleted successfully."})
        except Exception as e:
            return JsonResponse(
                {"message": "Location deletion failed.", "error": str(e)}
            )

