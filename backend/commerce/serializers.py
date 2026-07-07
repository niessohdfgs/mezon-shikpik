from rest_framework import serializers

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Purchase,
    Discount,
)



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "type",
            "price",
            "course",
            "pattern",
            "is_active",
        ]



class CartItemSerializer(serializers.ModelSerializer):

    product_detail = ProductSerializer(
        source="product",
        read_only=True
    )

    total_price = serializers.SerializerMethodField()


    class Meta:
        model = CartItem

        fields = [
            "id",
            "product",
            "product_detail",
            "quantity",
            "total_price",
        ]


    def get_total_price(self, obj):

        return obj.total_price()



class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Cart

        fields = [
            "id",
            "items",
            "total_price",
        ]


    def get_total_price(self, obj):

        return obj.total_price()



class OrderItemSerializer(serializers.ModelSerializer):

    product_detail = ProductSerializer(
        source="product",
        read_only=True
    )


    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_detail",
            "quantity",
            "price",
        ]



class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "total_price",
            "discount",
            "items",
            "created_at",
        ]



class PurchaseSerializer(serializers.ModelSerializer):

    product_detail = ProductSerializer(
        source="product",
        read_only=True
    )


    class Meta:
        model = Purchase

        fields = [
            "id",
            "product",
            "product_detail",
            "order",
            "created_at",
        ]



class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount

        fields = [
            "id",
            "code",
            "percent",
            "is_active",
        ]