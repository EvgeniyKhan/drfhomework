from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateView,
                             LessonDestroyView, LessonListView,
                             LessonRetrieveView, LessonUpdateView)

app_name = MaterialsConfig.name

router = SimpleRouter
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete')
] + router.urls
