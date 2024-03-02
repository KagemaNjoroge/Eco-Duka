import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from django.views import View

from .models import Category, Product
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class ProductView(View):
    def get(self, request: HttpRequest, id: int = None) -> JsonResponse:
        if id:
            product = get_object_or_404(Product, id=id)
            return JsonResponse(
                product.to_json(),
                safe=False,
                status=200,
            )
        else:
            # all products where merchant is the logged in user
            products = Product.objects.filter(merchant=request.user)
            return JsonResponse(
                [product.to_json() for product in products],
                safe=False,
                status=200,
            )

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        product = get_object_or_404(Product, id=id)
        product.delete()
        return JsonResponse({"message": "Product deleted"}, status=200)

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body
        data = json.loads(data)
        product = get_object_or_404(Product, id=id)
        # update the product with **data
        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.quantity = data["quantity"]
        category = get_object_or_404(Category, id=data["category"])
        merchant = request.user
        product.merchant = merchant
        product.category = category
        product.save()
        return JsonResponse(
            product.to_json(),
            safe=False,
            status=200,
        )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body
        data = json.loads(data)
        category = get_object_or_404(Category, id=data.get("category"))
        merchant = request.user
        product = Product(**data, category=category, merchant=merchant)
        product.save()
        return JsonResponse(
            product.to_json(),
            safe=False,
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request: HttpRequest, id: int = None) -> JsonResponse:
        if id:
            category = get_object_or_404(Category, id=id)
            return JsonResponse(
                category.to_json(),
                safe=False,
                status=200,
            )
        else:
            categories = Category.objects.all()
            return JsonResponse(
                [category.to_json() for category in categories],
                safe=False,
                status=200,
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body
        data = json.loads(data)
        category = Category(**data)
        category.save()
        return JsonResponse(
            category.to_json(),
            safe=False,
            status=201,
        )

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        data = request.body
        data = json.loads(data)
        category = get_object_or_404(Category, id=id)
        category.name = data.get("name", category.name)
        category.description = data.get("description", category.description)
        category.save()
        return JsonResponse(
            category.to_json(),
            safe=False,
            status=200,
        )

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        category = get_object_or_404(Category, id=id)
        category.delete()
        return JsonResponse({"message": "Category deleted"}, status=200)


def search(request: HttpRequest) -> JsonResponse:
    query = request.GET.get(key="search")
    if query:
        products = Product.objects.filter(name__icontains=query)
        products = [product.to_json() for product in products]
        return JsonResponse({"products": products}, safe=True, status=200)
    else:
        return JsonResponse(
            {"products": []},
            safe=True,
            status=200,
        )
