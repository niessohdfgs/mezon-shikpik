from django.contrib import admin
from .models import Course, Chapter, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter")