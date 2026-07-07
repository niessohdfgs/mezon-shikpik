
from django.db import models
from django.conf import settings


class Course(models.Model):

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField()

    thumbnail = models.ImageField(
        upload_to="courses/",
        null=True,
        blank=True
    )

    price = models.PositiveIntegerField()

    is_published = models.BooleanField(
        default=False
    )

    is_free = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.title



class Chapter(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="chapters"
    )

    title = models.CharField(
        max_length=255
    )

    order = models.PositiveIntegerField(
        default=0
    )


    class Meta:
        ordering = ["order"]



class Lesson(models.Model):

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    video = models.FileField(
        upload_to="videos/"
    )

    duration = models.PositiveIntegerField(
        default=0
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_free = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=False
    )


    class Meta:
        ordering = ["order"]





class CoursePurchase(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = (
            "user",
            "course"
        )

class LessonProgress(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    watched_seconds = models.PositiveIntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        unique_together = (
            "user",
            "lesson"
        )