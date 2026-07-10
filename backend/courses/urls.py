from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,

    AdminCourseListCreateView,
    AdminCourseDetailView,

    AdminChapterListCreateView,
    AdminChapterDetailView,

    AdminLessonListCreateView,
    AdminLessonDetailView,

    CourseContentView,

    LessonProgressView,
    LessonDetailView,
    LessonStreamView,
    LessonHeartbeatView,

    ContinueWatchingView,
)


urlpatterns = [

    # Public

    path(
        "",
        CourseListView.as_view()
    ),


    # Admin

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


    # Learning

    path(
        "<int:pk>/content/",
        CourseContentView.as_view()
    ),

    path(
        "lessons/<int:pk>/",
        LessonDetailView.as_view()
    ),

    path(
        "lessons/<int:pk>/stream/",
        LessonStreamView.as_view()
    ),

    path(
        "lessons/<int:pk>/heartbeat/",
        LessonHeartbeatView.as_view()
    ),

    path(
        "lessons/<int:lesson_id>/progress/",
        LessonProgressView.as_view()
    ),

    path(
        "continue-watching/",
        ContinueWatchingView.as_view()
    ),


    # Course Detail آخر باشد

    path(
        "<slug:slug>/",
        CourseDetailView.as_view()
    ),

]