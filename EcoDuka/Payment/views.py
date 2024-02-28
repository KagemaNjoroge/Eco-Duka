import json
from django.http import JsonResponse
from django.shortcuts import render

from User.models import CustomUser

from .models import PaymentPlan, Product, Payment
from .models import Sale
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class SalesView(View):
    def get(self, request, id: int = None):
        if id:
            sale = Sale.objects.get(id=id)
            return JsonResponse(sale.to_json())
        else:
            sales = Sale.objects.all()
            return JsonResponse([sale.to_json() for sale in sales], safe=False)

    def post(self, request):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        # products list
        amount = data["amount"]
        customer_id = data["customer"]
        customer = CustomUser.objects.get(id=customer_id)
        merchant_id = data["merchant"]
        merchant = CustomUser.objects.get(id=merchant_id)
        products_ids = data["products"]
        products = [Product.objects.get(id=product_id) for product_id in products_ids]
        sale = Sale(
            products=products, merchant=merchant, customer=customer, amount=amount
        )
        sale.save()
        return JsonResponse(sale.to_json())

    def delete(self, request, id):
        sale = Sale.objects.get(id=id)
        try:
            sale.delete()
            return JsonResponse({"message": "Sale deleted successfully."})
        except Exception as e:
            return JsonResponse({"message": "Sale deletion failed.", "error": str(e)})

    def put(self, request, id):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        sale = Sale.objects.get(id=id)
        sale.amount = data["amount"]
        sale.save()
        return JsonResponse(sale.to_json())


class PaymentPlanView(View):
    def get(self, request, id: int = None):
        if id:
            payment = PaymentPlan.objects.get(id=id)
            return JsonResponse(payment.to_json())
        else:
            payments = PaymentPlan.objects.all()
            return JsonResponse([payment.to_json() for payment in payments], safe=False)

    def post(self, request):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        period = data["period"]
        deposit = data["deposit"]
        percent = data["percent"]
        payment = PaymentPlan(period=period, deposit=deposit, percent=percent)
        payment.save()
        return JsonResponse(payment.to_json())

    def delete(self, request, id):
        payment = PaymentPlan.objects.get(id=id)
        try:
            payment.delete()
            return JsonResponse({"message": "Payment Plan deleted successfully."})
        except Exception as e:
            return JsonResponse(
                {"message": "Payment Plan deletion failed.", "error": str(e)}
            )

    def put(self, request, id):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        payment = PaymentPlan.objects.get(id=id)
        payment.period = data["period"]
        payment.deposit = data["deposit"]
        payment.percent = data["percent"]
        payment.save()
        return JsonResponse(payment.to_json())


class PaymentView(View):
    def get(self, request, id: int = None):
        if id:
            payment = Payment.objects.get(id=id)
            return JsonResponse(payment.to_json())
        else:
            payments = Payment.objects.all()
            return JsonResponse([payment.to_json() for payment in payments], safe=False)

    def delete(self, request, id):
        payment = Payment.objects.get(id=id)
        try:
            payment.delete()
            return JsonResponse({"message": "Payment deleted successfully."})
        except Exception as e:
            return JsonResponse(
                {"message": "Payment deletion failed.", "error": str(e)}
            )

    def post(self, request):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        user_id = data["user"]
        user = CustomUser.objects.get(id=user_id)
        amount = data["amount"]
        payment = Payment(user=user, amount=amount)
        payment.save()
        return JsonResponse(payment.to_json())

    def put(self, request, id):
        data = request.body.decode("utf-8")
        data = json.loads(data)
        payment = Payment.objects.get(id=id)
        payment.amount = data["amount"]
        payment.save()
        return JsonResponse(payment.to_json())
