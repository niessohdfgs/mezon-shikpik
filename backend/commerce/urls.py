from django.urls import path


from .views import (

    CartView,
    CartItemCreateView,
    CartItemDeleteView,

    CheckoutView,

    OrderListView,

    PurchaseListView,

    ProductListView,

    MyCoursesView,
    MyPatternsView,
    MyOrdersView,
    DiscountValidateView,
)



urlpatterns = [


    # Products

    path(
        "products/",
        ProductListView.as_view()
    ),


    # Cart

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


    # Checkout

    path(
        "checkout/",
        CheckoutView.as_view()
    ),


    # Orders

    path(
        "orders/",
        OrderListView.as_view()
    ),


    path(
        "orders/me/",
        MyOrdersView.as_view()
    ),


    # Purchases

    path(
        "purchases/",
        PurchaseListView.as_view()
    ),


    # Dashboard

    path(
        "my-courses/",
        MyCoursesView.as_view()
    ),


    path(
        "my-patterns/",
        MyPatternsView.as_view()
    ),
    path(
        "discounts/validate/",
        DiscountValidateView.as_view()
    ),
]