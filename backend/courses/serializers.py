from rest_framework import serializers
from .models import Course, Chapter, Lesson

from .models import LessonProgress


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"



class ChapterSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Chapter
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):

    chapters = ChapterSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Course
        fields = "__all__"




class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonProgress
        fields = "__all__"
        read_only_fields = [
            "user"
        ]