import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from django.views import View

from .models import Category, Product


class ProductView(View):
    def get(self, request: HttpRequest, id: int = None) -> JsonResponse:
        if id:
            product = get_object_or_404(Product, id=id)
            return JsonResponse(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "category": product.category.name,
                    "merchant": product.merchant.username,
                },
                safe=False,
                status=200,
            )
        else:
            # all products where merchant is the logged in user
            products = Product.objects.filter(merchant=request.user)
            return JsonResponse(
                [
                    {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "quantity": product.quantity,
                        "category": product.category.name,
                        "merchant": product.merchant.username,
                    }
                    for product in products
                ],
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
        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        category = get_object_or_404(Category, id=data.get("category"))
        merchant = request.user
        product.merchant = merchant
        product.category = category
        product.save()
        return JsonResponse(
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "category": product.category.name,
                "merchant": product.merchant.username,
            },
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
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "category": product.category.name,
                "merchant": product.merchant.username,
            },
            safe=False,
            status=201,
        )


class CategoryView(View):
    def get(self, request: HttpRequest, id: int = None) -> JsonResponse:
        if id:
            category = get_object_or_404(Category, id=id)
            return JsonResponse(
                {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                },
                safe=False,
                status=200,
            )
        else:
            categories = Category.objects.all()
            return JsonResponse(
                [
                    {
                        "id": category.id,
                        "name": category.name,
                        "description": category.description,
                    }
                    for category in categories
                ],
                safe=False,
                status=200,
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.body
        data = json.loads(data)
        category = Category(**data)
        category.save()
        return JsonResponse(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            },
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
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            },
            safe=False,
            status=200,
        )

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        category = get_object_or_404(Category, id=id)
        category.delete()
        return JsonResponse({"message": "Category deleted"}, status=200)
