from django.urls import path


from .views import (

    PatternListView,
    PatternDetailView,

    AdminPatternListCreateView,
    AdminPatternDetailView,

    PatternDownloadView,
)



urlpatterns = [


    path(
        "",
        PatternListView.as_view()
    ),



    path(
        "admin/",
        AdminPatternListCreateView.as_view()
    ),



    path(
        "admin/<int:pk>/",
        AdminPatternDetailView.as_view()
    ),



    path(
        "<int:pk>/download/",
        PatternDownloadView.as_view()
    ),



    path(
        "<slug:slug>/",
        PatternDetailView.as_view()
    ),

]