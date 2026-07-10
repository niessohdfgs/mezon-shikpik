from commerce.models import Purchase



class AccessService:


    @staticmethod
    def has_course_access(
        user,
        course
    ):

        return Purchase.objects.filter(

            user=user,

            product__course=course

        ).exists()



    @staticmethod
    def has_pattern_access(
        user,
        pattern
    ):

        return Purchase.objects.filter(

            user=user,

            product__pattern=pattern

        ).exists()



    @staticmethod
    def get_user_purchases(
        user
    ):

        return Purchase.objects.filter(
            user=user
        )