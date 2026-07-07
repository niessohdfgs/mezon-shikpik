from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .models import Pattern
from .serializers import PatternSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin

from .models import Pattern
from .serializers import PatternSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import HasPatternAccess



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



class AdminPatternListCreateView(ListCreateAPIView):

    queryset = Pattern.objects.all()

    serializer_class = PatternSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]



class AdminPatternDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Pattern.objects.all()

    serializer_class = PatternSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


class PatternDownloadView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasPatternAccess
    ]


    def get(self, request, pk):

        pattern = Pattern.objects.get(
            id=pk
        )


        return Response({
            "file": request.build_absolute_uri(
                pattern.file.url
            )
        })