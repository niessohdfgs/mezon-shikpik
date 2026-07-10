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



        # اگر زرین پال نداشتیم فعلا تستی

        return Response(
            {
                "payment_url":
                    f"/api/payment/fake-success/?order_id={order.id}",

                "authority":
                    f"TEST-{order.id}",

                "order_id":
                    order.id
            }
        )










class PaymentVerifyView(APIView):


    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        authority = request.GET.get(
            "Authority"
        )


        try:

            payment = Payment.objects.get(
                authority=authority,
                order__user=request.user
            )


        except Payment.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Payment not found"
                },
                status=404
            )



        payment.status = "success"

        payment.ref_id = authority

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
                "message":
                    "Payment successful",

                "ref_id":
                    payment.ref_id
            }
        )









class FakePaymentSuccessView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        order_id = request.GET.get(
            "order_id"
        )



        try:

            payment = Payment.objects.get(
                order_id=order_id,
                order__user=request.user
            )


        except Payment.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Payment not found"
                },
                status=404
            )




        payment.status = "success"

        payment.ref_id = (
            f"TEST-{payment.order.id}"
        )

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
                "message":
                    "Fake payment successful",

                "order_id":
                    order.id,

                "ref_id":
                    payment.ref_id
            }
        )