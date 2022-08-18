from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_account.constants import RoleData
from api_account.models import Account
from api_account.permissions import AdminPermission, BothPermission
from api_account.serializers import AccountSerializer
from api_base.views.MyBaseView import MyBaseView
from api_user.models import User
from api_user.serializer.User import RegisterUserSerializer, DetailUserSerializer, UpdateUserInfoSerializer


class UserViewSet(MyBaseView):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = DetailUserSerializer
    permission_classes = [IsAuthenticated]
    serializer_map = {
        'sign_up': [RegisterUserSerializer]
    }
    permission_map = {
        'sign_in': [],
        'sign_up': [],
        'update_user': [BothPermission],
        'delete_user': [AdminPermission]
    }

    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        account = Account.objects.filter(username=username)
        if account.exists():
            account = account.first()
            if not account.is_active:
                return Response({"details": "account is deactivated!"},
                                status=status.HTTP_400_BAD_REQUEST)
            if check_password(password, account.password):
                token = RefreshToken.for_user(account)
                response = {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token)
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response({"error_message": "invalid username/password"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    # Tao user loi thi xoa luon tai khoan vua dang ky
    @transaction.atomic
    def sign_up(self, request):
        user_data = request.data
        if user_data["role"].lower() == RoleData.USER.value.get("name").lower():
            user_data["role"] = RoleData.USER.value.get("id")
        else:
            user_data["role"] = RoleData.ADMIN.value.get("id")
        account_serializer = AccountSerializer(data=user_data)
        if account_serializer.is_valid(raise_exception=True):
            account = account_serializer.save()
            user_data['account'] = account.id.hex
            serializer = RegisterUserSerializer(data=user_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk):
        user = self.get_object()
        if user:
            account = Account.objects.get(id=user.account.id)
            if account is not None:
                account.delete()
            user.delete()
            return Response({"details": "Delete user successfully!"}, status=status.HTTP_200_OK)
        return Response({"details": "User is not defined yet. Please try again!"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def update_user(self, request):
        # update own info
        # get from the request is account
        account = request.user
        user = User.objects.get(account=account)
        if user:
            request_data = request.data
            if request_data:
                account.username = request_data.get('username')
                account.password = make_password(request_data.get('password'))
                account.save()
                new_info_serializer = UpdateUserInfoSerializer(user, data=request_data, partial=True)
                if new_info_serializer.is_valid(raise_exception=True):
                    new_info_serializer.save()
                    return Response({"Details": "User has been updated successfully"}, status=status.HTTP_200_OK)
            return Response({"Details": "No datas found!"}, status=status.HTTP_404_NOT_FOUND)

        # update info of other member
