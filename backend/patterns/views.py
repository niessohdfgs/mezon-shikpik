from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


from .models import Pattern

from .serializers import PatternSerializer

from .permissions import HasPatternAccess

from accounts.permissions import IsAdmin





# =========================
# Public Patterns
# =========================


class PatternListView(ListAPIView):

    queryset = Pattern.objects.filter(
        is_published=True
    )

    serializer_class = PatternSerializer





class PatternDetailView(RetrieveAPIView):

    queryset = Pattern.objects.filter(
        is_published=True
    )

    serializer_class = PatternSerializer

    lookup_field = "slug"







# =========================
# Admin Pattern
# =========================


class AdminPatternListCreateView(ListCreateAPIView):

    queryset = Pattern.objects.all()

    serializer_class = PatternSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]





class AdminPatternDetailView(
    RetrieveUpdateDestroyAPIView
):

    queryset = Pattern.objects.all()

    serializer_class = PatternSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]







# =========================
# Pattern Download
# =========================


class PatternDownloadView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasPatternAccess
    ]


    def get(
        self,
        request,
        pk
    ):

        pattern = get_object_or_404(
            Pattern,
            id=pk
        )


        return Response(
            {
                "file":
                request.build_absolute_uri(
                    pattern.file.url
                )
            }
        )