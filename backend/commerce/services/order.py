from django.db import transaction

from commerce.models import (
    Cart,
    Order,
    OrderItem,
    Payment,
    Purchase,
)

from commerce.services.discount import DiscountService




class OrderService:


    @staticmethod
    @transaction.atomic
    def create_order(
        user,
        discount=None
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



        # جلوگیری از خرید دوباره محصول

        for item in items:

            if Purchase.objects.filter(
                user=user,
                product=item.product
            ).exists():

                raise ValueError(
                    f"{item.product.title} already purchased"
                )



        # مبلغ اولیه

        total_price = sum(
            item.total_price()
            for item in items
        )



        # اعمال تخفیف

        if discount:

            total_price = DiscountService.calculate_final_price(
                total_price,
                discount
            )



        # ساخت سفارش

        order = Order.objects.create(

            user=user,

            total_price=total_price,

            discount=discount,

            status="pending"

        )



        # ساخت آیتم‌های سفارش

        for item in items:


            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )



        # ساخت پرداخت pending

        Payment.objects.create(

            order=order,

            amount=total_price,

            status="pending"

        )



        # سبد خرید خالی شود

        cart.items.all().delete()


        cart.discount = None

        cart.save()



        return order