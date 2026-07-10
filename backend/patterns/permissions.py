from rest_framework.permissions import BasePermission

from commerce.models import Purchase



class HasPatternAccess(BasePermission):


    def has_permission(
        self,
        request,
        view
    ):

        if not request.user.is_authenticated:
            return False


        pattern_id = view.kwargs.get(
            "pk"
        )


        return Purchase.objects.filter(

            user=request.user,

            product__pattern_id=pattern_id

        ).exists()