from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from api_task.models import Task
from api_task.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = PageNumberPagination
