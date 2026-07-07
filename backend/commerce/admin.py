from django.contrib import admin

from .models import (
    Product,
    Cart,
    CartItem,
    Discount,
    Order,
    OrderItem,
    Purchase,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "type",
        "price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "type",
        "is_active",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "created_at",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
    )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "percent",
        "is_active",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "created_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "price",
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "order",
        "created_at",
    )