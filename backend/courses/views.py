from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from django.shortcuts import get_object_or_404


from .models import (
    Course,
    Chapter,
    Lesson,
    LessonProgress,
)


from .serializers import (
    CourseSerializer,
    ChapterSerializer,
    LessonSerializer,
    LessonProgressSerializer,
)


from accounts.permissions import IsAdmin


from commerce.services.access import AccessService
from django.http import FileResponse
from django.http import FileResponse
from django.conf import settings
import os



# =========================
# Public Course
# =========================


class CourseListView(ListAPIView):

    queryset = Course.objects.filter(
        is_published=True
    ).prefetch_related(
        "chapters__lessons"
    )

    serializer_class = CourseSerializer


class CourseDetailView(RetrieveAPIView):

    queryset = Course.objects.filter(
        is_published=True
    ).prefetch_related(
        "chapters__lessons"
    )

    serializer_class = CourseSerializer

    lookup_field = "slug"






# =========================
# Admin Course
# =========================


class AdminCourseListCreateView(ListCreateAPIView):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]





class AdminCourseDetailView(
    RetrieveUpdateDestroyAPIView
):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]







# =========================
# Admin Chapter
# =========================


class AdminChapterListCreateView(ListCreateAPIView):

    queryset = Chapter.objects.all()

    serializer_class = ChapterSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]





class AdminChapterDetailView(
    RetrieveUpdateDestroyAPIView
):

    queryset = Chapter.objects.all()

    serializer_class = ChapterSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]







# =========================
# Admin Lesson
# =========================


class AdminLessonListCreateView(ListCreateAPIView):

    queryset = Lesson.objects.all()

    serializer_class = LessonSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]





class AdminLessonDetailView(
    RetrieveUpdateDestroyAPIView
):

    queryset = Lesson.objects.all()

    serializer_class = LessonSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]







# =========================
# Course Access
# =========================


class CourseContentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
        pk
    ):

        course = get_object_or_404(
            Course.objects.prefetch_related(
                "chapters__lessons"
            ),
            id=pk
        )


        has_access = AccessService.has_course_access(
            request.user,
            course
        )


        if not has_access:

            return Response(
                {
                    "error":
                    "You don't own this course"
                },
                status=403
            )


        return Response(
            CourseSerializer(course).data
        )







class MyCourseContentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
        pk
    ):

        course = get_object_or_404(
            Course.objects.prefetch_related(
                "chapters__lessons"
            ),
            id=pk
        )


        has_access = AccessService.has_course_access(
            request.user,
            course
        )


        if not has_access:

            return Response(
                {
                    "error":
                    "No access"
                },
                status=403
            )


        return Response(
            CourseSerializer(course).data
        )







# =========================
# Lesson Progress
# =========================


class LessonProgressView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request,
        lesson_id
    ):

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


    def get(
        self,
        request
    ):


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
    

# =========================
# Lesson Detail
# =========================


class LessonDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
        pk
    ):

        lesson = get_object_or_404(
            Lesson,
            id=pk,
            is_published=True
        )


        course = lesson.chapter.course


        if not AccessService.has_course_access(
            request.user,
            course
        ):

            return Response(
                {
                    "error":
                    "You don't own this course"
                },
                status=403
            )


        return Response(
            LessonSerializer(lesson).data
        )
    


# =========================
# Lesson Stream
# =========================


class LessonStreamView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
        pk
    ):

        lesson = get_object_or_404(
            Lesson,
            id=pk,
            is_published=True
        )


        course = lesson.chapter.course


        if not AccessService.has_course_access(
            request.user,
            course
        ):

            return Response(
                {
                    "error":
                    "You don't own this course"
                },
                status=403
            )


        return FileResponse(
            lesson.video.open("rb"),
            as_attachment=False,
            filename=lesson.video.name.split("/")[-1]
        )
    

# =========================
# Lesson Heartbeat
# =========================


class LessonHeartbeatView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request,
        pk
    ):

        lesson = get_object_or_404(
            Lesson,
            id=pk
        )


        course = lesson.chapter.course


        if not AccessService.has_course_access(
            request.user,
            course
        ):

            return Response(
                {
                    "error":
                    "You don't own this course"
                },
                status=403
            )


        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
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
    

class LessonStreamView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
        pk
    ):

        lesson = get_object_or_404(
            Lesson,
            id=pk,
            is_published=True
        )


        if not lesson.is_free:

            has_access = AccessService.has_course_access(
                request.user,
                lesson.chapter.course
            )


            if not has_access:

                return Response(
                    {
                        "error": "You don't own this course"
                    },
                    status=403
                )



        file_path = lesson.video.path


        if not os.path.exists(file_path):

            return Response(
                {
                    "error": "Video not found"
                },
                status=404
            )


        response = FileResponse(
            open(file_path, "rb"),
            content_type="video/mp4"
        )


        response["Content-Disposition"] = "inline"

        return response