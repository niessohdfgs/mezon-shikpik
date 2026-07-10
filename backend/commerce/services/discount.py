from django.utils import timezone

from commerce.models import Discount



class DiscountService:


    @staticmethod
    def get_discount(code):

        try:

            discount = Discount.objects.get(
                code=code
            )

        except Discount.DoesNotExist:

            raise ValueError(
                "Invalid discount code"
            )


        if not discount.is_active:

            raise ValueError(
                "Discount is inactive"
            )


        now = timezone.now()


        if discount.start_date:

            if now < discount.start_date:

                raise ValueError(
                    "Discount is not started yet"
                )


        if discount.end_date:

            if now > discount.end_date:

                raise ValueError(
                    "Discount has expired"
                )


        if discount.max_usage:

            if discount.used_count >= discount.max_usage:

                raise ValueError(
                    "Discount usage limit reached"
                )


        return discount



    @staticmethod
    def calculate_discount(
        amount,
        discount
    ):

        discount_amount = (
            amount *
            discount.percent
        ) // 100


        return discount_amount



    @staticmethod
    def calculate_final_price(
        amount,
        discount
    ):

        discount_amount = DiscountService.calculate_discount(
            amount,
            discount
        )


        return amount - discount_amount