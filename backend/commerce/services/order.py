from django.db import transaction

from commerce.models import (
    Cart,
    Order,
    OrderItem,
    Payment,
)



class OrderService:


    @staticmethod
    @transaction.atomic
    def create_order(
        user
    ):


        cart, created = Cart.objects.get_or_create(
            user=user
        )


        items = cart.items.select_related(
            "product"
        )


        if not items.exists():

            raise ValueError(
                "Cart is empty"
            )



        discount = cart.discount



        total_price = cart.total_price()



        order = Order.objects.create(

            user=user,

            total_price=total_price,

            discount=discount,

            status="pending"

        )



        for item in items:


            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )




        Payment.objects.create(

            order=order,

            amount=total_price,

            status="pending"

        )



        cart.items.all().delete()


        # حذف تخفیف بعد از تبدیل سبد به سفارش

        cart.discount = None

        cart.save()



        return order


# {
#     "user": {
#         "id": 6,
#         "phone": "09111111111",
#         "role": "student",
#         "is_staff": false,
#         "is_superuser": false,
#         "is_blocked": false
#     },
#     "session": "5074c8c557effaf486c818adc2f108dd0f7da6380280721f3cbffb7bd199eb32",
#     "expires_at": "2026-07-15T12:37:31.662527Z",
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NjEwNjI1MSwiaWF0IjoxNzgzNTE0MjUxLCJqdGkiOiI2NjFiMzc5YTU5Y2U0NjFkOTJjYTZiNjA1YjJkZmRhNSIsInVzZXJfaWQiOiI2In0.JEhlP499vzVDgr8lEA_FidTKolLWu6Z87shQeItwN20",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgzNTE2MDUxLCJpYXQiOjE3ODM1MTQyNTEsImp0aSI6ImRmZTcxYmMxYTFhNDQyNWY5ZmI4NDNkMDI0NDY5YjcxIiwidXNlcl9pZCI6IjYifQ.9nQGfUxQyqhx0wrzqLwhr4HUkNL52V_nSVC9twBUVRE"
# }