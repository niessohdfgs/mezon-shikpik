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



        if discount.start_date and now < discount.start_date:

            raise ValueError(
                "Discount is not started yet"
            )



        if discount.end_date and now > discount.end_date:

            raise ValueError(
                "Discount has expired"
            )



        if (
            discount.max_usage is not None
            and discount.used_count >= discount.max_usage
        ):

            raise ValueError(
                "Discount usage limit reached"
            )



        if discount.percent <= 0 or discount.percent > 100:

            raise ValueError(
                "Invalid discount percent"
            )



        return discount




    @staticmethod
    def calculate_discount(
        amount,
        discount
    ):


        return (
            amount *
            discount.percent
        ) // 100




    @staticmethod
    def calculate_final_price(
        amount,
        discount
    ):


        return (
            amount -
            DiscountService.calculate_discount(
                amount,
                discount
            )
        )