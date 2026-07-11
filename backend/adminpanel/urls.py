from django.urls import path


from .views import (

    AdminDashboardView,

    SalesAnalyticsView,

    UsersAnalyticsView,

    ProductsAnalyticsView,

)



urlpatterns = [


    path(
        "dashboard/",
        AdminDashboardView.as_view()
    ),



    path(
        "analytics/sales/",
        SalesAnalyticsView.as_view()
    ),



    path(
        "analytics/users/",
        UsersAnalyticsView.as_view()
    ),



    path(
        "analytics/products/",
        ProductsAnalyticsView.as_view()
    ),


]