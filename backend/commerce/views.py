from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)


from rest_framework.permissions import IsAuthenticated


from .models import (
    Cart,
    CartItem,
    Order,
    Product,
    Purchase,
    Discount,
)


from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    PurchaseSerializer,
)


from .services.order import OrderService
from .services.discount import DiscountService


from courses.models import Course
from courses.serializers import CourseSerializer

from patterns.models import Pattern
from patterns.serializers import PatternSerializer




# =========================
# Cart
# =========================


class CartView(RetrieveAPIView):

    serializer_class = CartSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        return cart







# =========================
# Add Cart Item
# =========================


class CartItemCreateView(CreateAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def perform_create(
        self,
        serializer
    ):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )


        serializer.save(
            cart=cart
        )







# =========================
# Remove Cart Item
# =========================


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

        try:

            order = OrderService.create_order(
                request.user
            )


        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
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
            status=status.HTTP_201_CREATED
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
        ).order_by(
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

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = CourseSerializer


    def get_queryset(self):

        return Course.objects.filter(
            product__purchase__user=self.request.user
        ).distinct()





class MyPatternsView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = PatternSerializer


    def get_queryset(self):

        return Pattern.objects.filter(
            product__purchase__user=self.request.user
        ).distinct()





class MyOrdersView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = OrderSerializer


    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by(
            "-id"
        )








# =========================
# Discount Validate
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
                "code": discount.code,
                "percent": discount.percent
            }
        )








# =========================
# Apply Discount
# =========================


class ApplyDiscountView(APIView):

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








# =========================
# Remove Discount
# =========================


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