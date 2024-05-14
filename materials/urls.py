from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    CourseCreateAPIView,
    CourseListAPIView,
    LessonCreateAPIView,
    SubscriptionAPIView,
)

app_name = "materials"

router = routers.DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    # Lesson-Уроки
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/view/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-view"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
    # Course-Курсы
    path("course/create/", CourseCreateAPIView.as_view(), name="course-create"),
    path("course/list/<int:pk>/", CourseListAPIView.as_view(), name="course-list"),
    # Subscription
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
] + router.urls
