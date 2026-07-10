from rest_framework.permissions import BasePermission

from commerce.models import Purchase



class HasCourseAccess(BasePermission):


    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        if not request.user.is_authenticated:

            return False


        return Purchase.objects.filter(
            user=request.user,
            product__course=obj
        ).exists()