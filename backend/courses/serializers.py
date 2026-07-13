from rest_framework import serializers

from .models import (
    Course,
    Chapter,
    Lesson,
    LessonProgress
)



class LessonSerializer(serializers.ModelSerializer):

    class Meta:

        model = Lesson

        fields = [
            "id",
            "title",
            "description",
            "duration",
            "order",
            "is_free",
            "is_published",
        ]




class ChapterSerializer(serializers.ModelSerializer):

    lessons = serializers.SerializerMethodField()


    class Meta:

        model = Chapter

        fields = [
            "id",
            "title",
            "order",
            "lessons",
        ]


    def get_lessons(
        self,
        obj
    ):

        lessons = obj.lessons.filter(
            is_published=True
        )


        return LessonSerializer(
            lessons,
            many=True
        ).data





class CourseSerializer(serializers.ModelSerializer):

    chapters = ChapterSerializer(
        many=True,
        read_only=True
    )


    class Meta:

        model = Course

        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail",
            "price",
            "is_published",
            "is_free",
            "chapters",
        ]





class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:

        model = LessonProgress

        fields = "__all__"

        read_only_fields = [
            "user"
        ]