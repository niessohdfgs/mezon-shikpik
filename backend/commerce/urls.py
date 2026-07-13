from django.urls import path


from .views import (

    CartView,
    CartItemCreateView,
    CartItemDeleteView,

    CheckoutView,

    OrderListView,
    OrderDetailView,

    PurchaseListView,

    ProductListView,

    MyCoursesView,
    MyPatternsView,
    MyOrdersView,

    DiscountValidateView,

    WishlistView,
    WishlistCreateView,
    WishlistDeleteView,

    PaymentCreateView,
    PaymentVerifyView,
    PaymentCallbackView,
    AdminOrderListView,
    AdminOrderDetailView,

    AdminDiscountListCreateView,
    AdminDiscountDetailView,
    AdminPurchaseListView,
)


urlpatterns = [

    # =========================
    # Products
    # =========================

    path(
        "products/",
        ProductListView.as_view()
    ),



    # =========================
    # Cart
    # =========================

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



    # =========================
    # Checkout
    # =========================

    path(
        "checkout/",
        CheckoutView.as_view()
    ),



    # =========================
    # Orders
    # =========================

    path(
        "orders/",
        OrderListView.as_view()
    ),


    path(
        "orders/me/",
        MyOrdersView.as_view()
    ),


    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view()
    ),



    # =========================
    # Purchases
    # =========================

    path(
        "purchases/",
        PurchaseListView.as_view()
    ),



    # =========================
    # User Dashboard
    # =========================

    path(
        "my-courses/",
        MyCoursesView.as_view()
    ),


    path(
        "my-patterns/",
        MyPatternsView.as_view()
    ),



    # =========================
    # Discount
    # =========================

    path(
        "discounts/validate/",
        DiscountValidateView.as_view()
    ),



    # =========================
    # Wishlist
    # =========================

    path(
        "wishlist/",
        WishlistView.as_view()
    ),


    path(
        "wishlist/add/",
        WishlistCreateView.as_view()
    ),


    path(
        "wishlist/<int:productId>/",
        WishlistDeleteView.as_view()
    ),


    path(
        "payments/create/",
        PaymentCreateView.as_view()
    ),


    path(
        "payments/verify/",
        PaymentVerifyView.as_view()
    ),


    path(
        "payments/callback/",
        PaymentCallbackView.as_view()
    ),
    # =========================
    # Admin Orders
    # =========================


    path(
        "admin/orders/",
        AdminOrderListView.as_view()
    ),


    path(
        "admin/orders/<int:pk>/",
        AdminOrderDetailView.as_view()
    ),
    
    path(
        "admin/discounts/",
        AdminDiscountListCreateView.as_view()
    ),


    path(
        "admin/discounts/<int:pk>/",
        AdminDiscountDetailView.as_view()
    ),

    path(
        "admin/purchases/",
        AdminPurchaseListView.as_view()
    ),
]