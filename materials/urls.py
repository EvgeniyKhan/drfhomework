from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView, CourseCreateAPIView, CourseListAPIView,
                             LessonCreateAPIView)

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    #Lesson-Уроки
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    #Course-Курсы
    path('course/create', CourseCreateAPIView.as_view(), name='course_create'),
    path('course/list/<int:pk>/', CourseListAPIView.as_view(), name='course_list'),
] + router.urls
