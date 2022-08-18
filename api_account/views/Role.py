from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from api_account.models import Role
from api_account.serializers import RoleSerializer


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset
