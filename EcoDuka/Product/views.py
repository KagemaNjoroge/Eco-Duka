from itertools import product
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render

from django.views import View

from EcoDuka.Product.models import Category, Product


# Create your views here.
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
