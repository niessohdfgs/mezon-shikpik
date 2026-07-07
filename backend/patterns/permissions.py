from rest_framework.permissions import BasePermission
from .models import PatternPurchase


class HasPatternAccess(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        pattern_id = view.kwargs.get("pk")

        return PatternPurchase.objects.filter(
            user=request.user,
            pattern_id=pattern_id
        ).exists()