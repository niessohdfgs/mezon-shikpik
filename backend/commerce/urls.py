from django.urls import path

from .views import (
    ProductListView,
    CartView,
    CartItemCreateView,
    CartItemDeleteView,
    CheckoutView,
    OrderListView,
    PurchaseListView,
)

from .payment_views import (
    PaymentRequestView,
    PaymentVerifyView,
)


urlpatterns = [

    path(
        "products/",
        ProductListView.as_view()
    ),


    path(
        "cart/",
        CartView.as_view()
    ),


    path(
        "cart/items/",
        CartItemCreateView.as_view()
    ),


    path(
        "cart/items/<int:pk>/",
        CartItemDeleteView.as_view()
    ),


    path(
        "checkout/",
        CheckoutView.as_view()
    ),


    path(
        "orders/",
        OrderListView.as_view()
    ),


    path(
        "purchases/",
        PurchaseListView.as_view()
    ),


    path(
        "payment/request/",
        PaymentRequestView.as_view()
    ),


    path(
        "payment/verify/",
        PaymentVerifyView.as_view()
    ),

]