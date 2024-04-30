from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet,
                             LessonDestroyView, LessonListView,
                             LessonRetrieveView, LessonUpdateView, CourseCreateView, CourseListView,
                             LessonCreateAPIView)

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    #Lesson-Уроки
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete'),

    #Course-Курсы
    path('course/create', CourseCreateView.as_view(), name='course_create'),
    path('course/list/<int:pk>/', CourseListView.as_view(), name='course_list'),
] + router.urls
