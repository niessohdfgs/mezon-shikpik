from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
)


from django.db.models import (
    Sum,
    Count,
)


from accounts.models import User
from accounts.permissions import IsAdmin


from courses.models import Course

from patterns.models import Pattern


from commerce.models import (
    Order,
    Product,
)





# =========================
# Dashboard
# =========================


class AdminDashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]


    def get(
        self,
        request
    ):


        total_users = User.objects.count()


        total_courses = Course.objects.count()


        total_patterns = Pattern.objects.count()


        total_orders = Order.objects.count()


        paid_orders = Order.objects.filter(
            status="paid"
        ).count()



        total_sales = Order.objects.filter(
            status="paid"
        ).aggregate(
            total=Sum("total_price")
        )["total"] or 0



        return Response(
            {

                "users":
                total_users,


                "courses":
                total_courses,


                "patterns":
                total_patterns,


                "orders":
                total_orders,


                "paid_orders":
                paid_orders,


                "total_sales":
                total_sales,

            }
        )









# =========================
# Sales Analytics
# =========================


class SalesAnalyticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]


    def get(
        self,
        request
    ):


        return Response(
            {

                "total_sales":
                Order.objects.filter(
                    status="paid"
                ).aggregate(
                    total=Sum("total_price")
                )["total"] or 0,



                "paid_orders":
                Order.objects.filter(
                    status="paid"
                ).count(),



                "pending_orders":
                Order.objects.filter(
                    status="pending"
                ).count(),



                "failed_orders":
                Order.objects.filter(
                    status="failed"
                ).count(),

            }
        )









# =========================
# Users Analytics
# =========================


class UsersAnalyticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]


    def get(
        self,
        request
    ):


        return Response(
            {

                "total_users":
                User.objects.count(),



                "students":
                User.objects.filter(
                    role="student"
                ).count(),



                "admins":
                User.objects.filter(
                    role="admin"
                ).count(),



                "blocked_users":
                User.objects.filter(
                    is_blocked=True
                ).count(),

            }
        )









# =========================
# Products Analytics
# =========================


class ProductsAnalyticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]


    def get(
        self,
        request
    ):


        products = Product.objects.annotate(

            sales_count=Count(
                "order_items"
            )

        ).order_by(
            "-sales_count"
        )[:10]



        data = []



        for product in products:

            data.append(
                {

                    "id":
                    product.id,


                    "title":
                    product.title,


                    "type":
                    product.type,


                    "price":
                    product.price,


                    "sales_count":
                    product.sales_count,

                }
            )



        return Response(
            data
        )