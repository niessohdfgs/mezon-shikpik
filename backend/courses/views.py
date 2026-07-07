from .models import (
    Course,
    Chapter,
    Lesson
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Chapter
from .models import Course
from .serializers import CourseSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import HasCourseAccess
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin
from .serializers import (
    CourseSerializer,
    ChapterSerializer,
    LessonSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LessonProgress
from .serializers import LessonProgressSerializer

from .models import CoursePurchase

class CourseListView(ListAPIView):
    queryset = Course.objects.filter(
        is_published=True
    )
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.filter(
        is_published=True
    )
    serializer_class = CourseSerializer
    lookup_field = "slug"


class AdminCourseListCreateView(ListCreateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]



class AdminCourseDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]




class AdminChapterListCreateView(ListCreateAPIView):

    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]



class AdminChapterDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


class AdminLessonListCreateView(ListCreateAPIView):

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]



class AdminLessonDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

class CourseContentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request, pk):

        course = Course.objects.get(
            id=pk
        )

        has_access = Purchase.objects.filter(
            user=request.user,
            course=course
        ).exists()


        if not has_access:
            return Response(
                {
                    "error":"You don't own this course"
                },
                status=403
            )


        serializer = CourseSerializer(course)

        return Response(
            serializer.data
        )
    

class MyCourseContentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request, pk):

        access = CoursePurchase.objects.filter(
            user=request.user,
            course_id=pk
        ).exists()


        if not access:
            return Response(
                {
                    "error": "No access"
                },
                status=403
            )


        course = Course.objects.get(
            id=pk
        )


        return Response(
            CourseSerializer(course).data
        )
    

class LessonProgressView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request, lesson_id):

        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson_id=lesson_id
        )


        progress.watched_seconds = request.data.get(
            "watched_seconds",
            progress.watched_seconds
        )

        progress.completed = request.data.get(
            "completed",
            progress.completed
        )

        progress.save()


        return Response(
            LessonProgressSerializer(progress).data
        )
    

class ContinueWatchingView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        progress = LessonProgress.objects.filter(
            user=request.user,
            completed=False
        ).order_by(
            "-updated_at"
        ).first()


        if not progress:
            return Response(
                {}
            )


        return Response(
            LessonProgressSerializer(progress).data
        )