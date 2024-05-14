from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import URLValidate
from users.serliazers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [URLValidate(field="video_link")]

        def create(self, validated_data):
            user = self.context["request"].user
            lesson = Lesson(**validated_data)
            lesson.owner = user
            lesson.save()
            return lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def create(self, validated_data):
        user = self.context["request"].user
        course = Course(**validated_data)
        course.owner = user
        course.save()
        return course

    def get_subscription(self, instance):
        user = self.context["request"].user
        return (
            Subscription.objects.all()
            .filter(user=user)
            .filter(course=instance)
            .exists()
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
