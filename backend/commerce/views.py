from django.conf import settings
from django.shortcuts import get_object_or_404


from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework.permissions import IsAuthenticated


from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)



from .models import (
    Cart,
    CartItem,
    Order,
    Product,
    Purchase,
    Wishlist,
    Payment,
    Discount,
)



from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    PurchaseSerializer,
    WishlistSerializer,
    DiscountSerializer,
)



from .services.order import OrderService

from .services.discount import DiscountService


from .services.zarinpal import (
    request_payment,
    verify_payment,
    get_payment_url,
)



from courses.models import Course
from courses.serializers import CourseSerializer


from patterns.models import Pattern
from patterns.serializers import PatternSerializer


from accounts.permissions import IsAdmin







# =========================
# Cart
# =========================


class CartView(RetrieveDestroyAPIView):

    serializer_class = CartSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        return Cart.objects.prefetch_related(
            "items__product"
        ).get(
            id=cart.id
        )



    def perform_destroy(
        self,
        instance
    ):

        instance.items.all().delete()

        instance.discount = None

        instance.save()










# =========================
# Cart Items
# =========================


class CartItemCreateView(CreateAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        product_id = request.data.get(
            "product"
        )


        quantity = int(
            request.data.get(
                "quantity",
                1
            )
        )


        product = get_object_or_404(
            Product,
            id=product_id
        )


        if not product.is_active:

            return Response(
                {
                    "error": "Product is inactive"
                },
                status=400
            )



        if Purchase.objects.filter(
            user=request.user,
            product=product
        ).exists():

            return Response(
                {
                    "error": "Product already purchased"
                },
                status=400
            )



        if quantity < 1:

            return Response(
                {
                    "error": "Invalid quantity"
                },
                status=400
            )



        item, created = CartItem.objects.get_or_create(

            cart=cart,

            product=product,

            defaults={
                "quantity": quantity
            }

        )


        if not created:

            item.quantity += quantity

            item.save()



        return Response(
            CartItemSerializer(item).data,
            status=201
        )


class CartItemDeleteView(DestroyAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )









# =========================
# Checkout
# =========================


class CheckoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):

        discount = None


        discount_code = request.data.get(
            "discount_code"
        )


        if discount_code:

            discount = DiscountService.get_discount(
                discount_code
            )


            if not discount:

                return Response(
                    {
                        "error":
                        "Invalid discount"
                    },
                    status=400
                )


        try:

            order = OrderService.create_order(
                request.user,
                discount=discount
            )


        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=400
            )


        return Response(
            {
                "message":
                "Order created successfully",

                "order_id":
                order.id,

                "amount":
                order.total_price,

                "status":
                order.status
            },

            status=201
        )
    

# =========================
# Orders
# =========================


class OrderListView(ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).select_related(
            "payment"
        ).prefetch_related(
            "items__product"
        ).order_by(
            "-id"
        )







class OrderDetailView(RetrieveAPIView):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).select_related(
            "payment"
        ).prefetch_related(
            "items__product"
        )









# =========================
# Admin Orders
# =========================


class AdminOrderListView(ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = Order.objects.all().select_related(
        "payment"
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-id"
    )







class AdminOrderDetailView(RetrieveAPIView):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = Order.objects.all().select_related(
        "payment"
    ).prefetch_related(
        "items__product"
    )


class AdminPurchaseListView(ListAPIView):

    serializer_class = PurchaseSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    queryset = Purchase.objects.all().order_by(
        "-id"
    )






# =========================
# Purchases
# =========================


class PurchaseListView(ListAPIView):

    serializer_class = PurchaseSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Purchase.objects.filter(
            user=self.request.user
        ).select_related(
            "product"
        ).order_by(
            "-id"
        )









# =========================
# Products
# =========================


class ProductListView(ListAPIView):

    serializer_class = ProductSerializer


    def get_queryset(self):

        return Product.objects.filter(
            is_active=True
        )









# =========================
# User Dashboard
# =========================


class MyCoursesView(ListAPIView):

    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Course.objects.filter(
            product__purchase__user=self.request.user
        ).distinct()







class MyPatternsView(ListAPIView):

    serializer_class = PatternSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Pattern.objects.filter(
            product__purchase__user=self.request.user
        ).distinct()







class MyOrdersView(ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by(
            "-id"
        )









# =========================
# Discount
# =========================


class DiscountValidateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):

        code = request.data.get(
            "code"
        )


        try:

            discount = DiscountService.get_discount(
                code
            )


        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=400
            )



        return Response(
            {
                "valid": True,

                "code":
                discount.code,

                "percent":
                discount.percent
            }
        )









class ApplyDiscountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        try:

            discount = DiscountService.get_discount(
                request.data.get("code")
            )


        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=400
            )



        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        cart.discount = discount

        cart.save()



        return Response(
            {
                "message":
                "Discount applied",

                "code":
                discount.code,

                "percent":
                discount.percent
            }
        )









class RemoveDiscountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def delete(
        self,
        request
    ):


        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        cart.discount = None

        cart.save()



        return Response(
            {
                "message":
                "Discount removed"
            }
        )









# =========================
# Admin Discounts
# =========================


class AdminDiscountListCreateView(ListCreateAPIView):

    serializer_class = DiscountSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = Discount.objects.all().order_by(
        "-id"
    )








class AdminDiscountDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = DiscountSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = Discount.objects.all()



# =========================
# Wishlist
# =========================


class WishlistView(ListAPIView):

    serializer_class = WishlistSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related(
            "product"
        ).order_by(
            "-id"
        )




class WishlistCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        product_id = request.data.get(
            "product"
        )


        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )


        wishlist, created = Wishlist.objects.get_or_create(

            user=request.user,

            product=product

        )


        return Response(
            WishlistSerializer(
                wishlist
            ).data,

            status=201 if created else 200
        )




class WishlistDeleteView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def delete(
        self,
        request,
        productId
    ):


        Wishlist.objects.filter(

            user=request.user,

            product_id=productId

        ).delete()



        return Response(
            {
                "message":
                "Removed from wishlist"
            }
        )









# =========================
# Payment
# =========================


class PaymentCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        order = get_object_or_404(

            Order,

            id=request.data.get(
                "order_id"
            ),

            user=request.user

        )



        payment = order.payment



        result = request_payment(

            settings.ZARINPAL_MERCHANT_ID,

            payment.amount,

            settings.ZARINPAL_CALLBACK_URL,

            f"Order {order.id}"

        )



        authority = result.get(
            "data",
            {}
        ).get(
            "authority"
        )



        if not authority:

            return Response(
                {
                    "detail":
                    "Payment request failed",

                    "response":
                    result
                },

                status=400
            )



        payment.authority = authority

        payment.gateway_response = result

        payment.save()



        return Response(
            {
                "payment_url":
                get_payment_url(
                    authority
                ),

                "authority":
                authority
            }
        )









class PaymentVerifyView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request
    ):


        authority = request.query_params.get(
            "Authority"
        )


        payment = get_object_or_404(

            Payment,

            authority=authority,

            order__user=request.user

        )


        # جلوگیری از Verify دوباره

        if payment.status == "success":

            return Response(
                {
                    "status": "already_verified",

                    "ref_id": payment.ref_id
                }
            )



        result = verify_payment(

            settings.ZARINPAL_MERCHANT_ID,

            payment.amount,

            authority

        )



        payment.gateway_response = result



        if result.get("data"):


            payment.status = "success"


            payment.ref_id = result["data"].get(
                "ref_id"
            )



            order = payment.order


            order.status = "paid"

            order.save()



            # ساخت Purchase

            for item in order.items.all():


                Purchase.objects.get_or_create(

                    user=order.user,

                    product=item.product,

                    order=order

                )



            # مصرف تخفیف بعد از پرداخت موفق

            if order.discount:

                order.discount.used_count += 1

                order.discount.save()



        else:


            payment.status = "failed"



        payment.save()



        return Response(

            {
                "status": payment.status,

                "ref_id": payment.ref_id
            }

        )







class PaymentCallbackView(APIView):


    def get(
        self,
        request
    ):


        return Response(
            {
                "authority":
                request.query_params.get(
                    "Authority"
                ),

                "status":
                request.query_params.get(
                    "Status"
                )
            }
        )






