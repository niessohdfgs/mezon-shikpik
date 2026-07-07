from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    PurchaseSerializer,
)

from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView
from .models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
    Product,
    Purchase,
)

from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    PurchaseSerializer,
)


# -------------------------
# Cart
# -------------------------

class CartView(RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        return cart



# -------------------------
# Add item to cart
# -------------------------

class CartItemCreateView(CreateAPIView):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )


        serializer.save(
            cart=cart
        )



# -------------------------
# Remove cart item
# -------------------------

class CartItemDeleteView(DestroyAPIView):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )



# -------------------------
# Checkout
# -------------------------

class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]


    @transaction.atomic
    def post(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        items = cart.items.all()


        if not items.exists():

            return Response(
                {
                    "detail": "Cart is empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        total = cart.total_price()


        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status="pending"
        )


        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )


        items.delete()


        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "amount": total
            },
            status=status.HTTP_201_CREATED
        )


# -------------------------
# Orders
# -------------------------

class OrderListView(ListAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by("-id")



# -------------------------
# Purchase list
# -------------------------

class PurchaseListView(ListAPIView):

    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Purchase.objects.filter(
            user=self.request.user
        ).order_by("-id")
    


class ProductListView(ListAPIView):

    serializer_class = ProductSerializer


    def get_queryset(self):

        return Product.objects.filter(
            is_active=True
        )
    

