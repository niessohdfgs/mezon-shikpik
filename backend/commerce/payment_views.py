from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Order,
    Payment,
    Purchase,
)

from .services.zarinpal import (
    request_payment,
    verify_payment,
    get_payment_url,
)



class PaymentRequestView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        order_id = request.data.get(
            "order_id"
        )


        try:

            order = Order.objects.get(
                id=order_id,
                user=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {
                    "detail": "Order not found"
                },
                status=404
            )


        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "amount": order.total_price
            }
        )


        result = request_payment(
            merchant_id=settings.ZARINPAL_MERCHANT_ID,
            amount=payment.amount,
            callback_url=settings.ZARINPAL_CALLBACK_URL,
            description=f"Order #{order.id}"
        )


        if result.get("data"):

            authority = result["data"]["authority"]

            payment.authority = authority
            payment.save()


            return Response(
                {
                    "payment_url": get_payment_url(authority),
                    "authority": authority,
                    "order_id": order.id
                }
            )


        return Response(
            {
                "detail": "Zarinpal error",
                "response": result
            },
            status=400
        )





class PaymentVerifyView(APIView):


    def get(self, request):

        authority = request.GET.get(
            "Authority"
        )

        status_param = request.GET.get(
            "Status"
        )


        if status_param != "OK":

            return Response(
                {
                    "detail": "Payment canceled"
                },
                status=400
            )


        try:

            payment = Payment.objects.get(
                authority=authority
            )

        except Payment.DoesNotExist:

            return Response(
                {
                    "detail": "Payment not found"
                },
                status=404
            )


        result = verify_payment(
            merchant_id=settings.ZARINPAL_MERCHANT_ID,
            amount=payment.amount,
            authority=authority
        )


        if result.get("data"):

            payment.status = "success"
            payment.ref_id = result["data"]["ref_id"]
            payment.save()


            order = payment.order

            order.status = "paid"
            order.save()


            for item in order.items.all():

                Purchase.objects.get_or_create(
                    user=order.user,
                    product=item.product,
                    order=order
                )


            return Response(
                {
                    "message": "Payment successful",
                    "ref_id": payment.ref_id
                }
            )


        payment.status = "failed"
        payment.save()


        return Response(
            {
                "detail": "Payment failed"
            },
            status=400
        )