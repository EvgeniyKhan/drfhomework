from rest_framework import generics, viewsets, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CourseAndLessonPagination
from materials.permissons import IsModerator, IsOwner
from materials.serliazers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPagination
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Возвращает список классов разрешений в зависимости от текущего действия.
        :return: Список классов разрешений для текущего действия.
        """
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Возвращает список объектов в базе данных в виде сериализованных данных.

        :param request: Объект запроса.
        :type request: Request
        :return: Список сериализованных данных.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        """
        Создает новый объект в базе данных и устанавливает текущего пользователя как владельца.

        :param serializer: Сериализатор для создания объекта.
        :type serializer: Serializer
        """
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPagination


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Создает новый объект (например, урок) в базе данных и устанавливает текущего пользователя как владельца.

        :param serializer: Сериализатор для создания объекта.
        :type serializer: Serializer
        """
        new_lessons = serializer.save()
        new_lessons.owner = self.request.user
        new_lessons.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CourseAndLessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает запрос к базе данных для получения объектов Lesson в зависимости от прав доступа текущего пользователя.

        Если текущий пользователь принадлежит группе 'moderator', возвращает все уроки. Иначе возвращает уроки, которые принадлежат текущему пользователю.

        :return: Запрос к базе данных для получения объектов Lesson.
        """
        if self.request.user.groups.filter(groups__name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Возвращает список всех уроков из базы данных в виде сериализованных данных.

        :param request: Объект запроса.
        :type request: Request
        :return: Список сериализованных данных уроков.
        """
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response({"lesson": serializer.data})


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Создает подписку на курс или удаляет существующую подписку пользователя.

        Parameters:
        - request: Запрос API, содержащий информацию о пользователе и курсе для подписки.
        - args: Дополнительные аргументы, если таковые есть.
        - kwargs: Дополнительные именованные аргументы, если таковые есть.

        Returns:
        - Response: Сообщение о статусе операции и соответствующий HTTP статус.

        Raises:
        - HTTP404: Если курс с указанным ID не найден.
        """
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        sub_item, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )

        if created:
            message = "Подписка на курс успешно добавлена"
            status_code = (
                status.HTTP_201_CREATED
            )  # Код 201 для успешного создания ресурса
        else:
            sub_item.delete()
            message = "Подписка на курс успешно удалена"
            status_code = (
                status.HTTP_204_NO_CONTENT
            )  # Код 204 для успешного удаления ресурса

        return Response({"message": message}, status=status_code)
