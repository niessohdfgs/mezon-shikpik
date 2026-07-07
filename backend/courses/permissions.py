from rest_framework.permissions import BasePermission
from commerce.models import Purchase


class HasCourseAccess(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        return Purchase.objects.filter(
            user=request.user,
            course=obj
        ).exists()