from django.urls import path
from .views import (
    AdminChapterListCreateView,
    AdminChapterDetailView
)

from .views import *


urlpatterns = [

    path(
        "",
        CourseListView.as_view()
    ),

    path(
        "<slug:slug>/",
        CourseDetailView.as_view()
    ),
    path(
        "admin/",
        AdminCourseListCreateView.as_view()
    ),

    path(
        "admin/<int:pk>/",
        AdminCourseDetailView.as_view()
        ),
    path(
        "admin/chapters/",
        AdminChapterListCreateView.as_view()
    ),

    path(
        "admin/chapters/<int:pk>/",
        AdminChapterDetailView.as_view()
    ),
    path(
        "admin/lessons/",
        AdminLessonListCreateView.as_view()
    ),

    path(
        "admin/lessons/<int:pk>/",
        AdminLessonDetailView.as_view()
    ),
    path(
        "<int:pk>/content/",
        CourseContentView.as_view()
    ),
    path(
        "<int:pk>/content/",
        MyCourseContentView.as_view()
    ),

    path(
        "lessons/<int:lesson_id>/progress/",
        LessonProgressView.as_view()
    ),

    path(
        "continue-watching/",
        ContinueWatchingView.as_view()
    ),
]