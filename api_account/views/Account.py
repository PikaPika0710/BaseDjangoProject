from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_account.models import Account, Role
from api_account.serializers import AccountSerializer
from api_task.models import Task
from api_task.serializers import TaskSerializer


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    pagination_class = PageNumberPagination

    # get all accounts
    @action(detail=True, methods=['get'])
    def get_queryset(self):
        queryset = Account.objects.filter(is_active=True)
        return queryset

    # get account details
    @action(detail=True, methods=['get'])
    def get_account_detail(self, request, pk):
        account = self.get_object()
        return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)

    # sign_up function
    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        account = Account.objects.filter(username=username, password=password)
        if account.exists():
            # return Response({"message": "Logging successfully"}, status=status.HTTP_200_OK)
            # return Response(AccountSerializer(account.first()).data, status=status.HTTP_200_OK)
            account = account.first()
            token = RefreshToken.for_user(account)
            response = {
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error_message": "invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def add_role(self, request):
        # check trung
        name = request.data.get('name')
        role = Role(name=name)
        role.save()
        return Response(status=status.HTTP_201_CREATED)

    # get tasks of 1 account
    @action(detail=True, methods=['get'], url_path='tasks')
    def get_tasks(self, request, pk):
        # If account is admin, show all tasks of all users
        try:
            account = self.get_object()
            # account = Account.objects.get(pk=pk)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if account.role.name == 'admin':
                tasks = Task.objects.all()
            else:
                tasks = account.tasks

            return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)

    # add task
    @action(detail=True, methods=['post'])
    def add_task(self, request, pk):
        try:
            account = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tasks = request.data.get('tasks')
            if tasks is not None:
                for task in tasks:
                    t, _ = Task.objects.get_or_create(task=task, account_id=account.id)
                    account.tasks.add(t)
                account.save()
                return Response(self.serializer_class(account).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # update task
    @action(detail=True, methods=['post'])
    def update_task(self, request, pk):
        try:
            account = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            task_id = request.data.get("id")
            try:
                task = account.tasks.get(pk=task_id)
            except Exception:
                return Response({"error message": "Account doesn't have task with that id!!!"})
            else:
                task.task = request.data.get("task")
                task.is_done = request.data.get("is_done")
                task.note = request.data.get("note")
                task.account_id = request.data.get("account_id")
                task.save()
                return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    # delete task
    @action(detail=True, methods=['post'])
    def delete_task(self, request, pk):
        try:
            account = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            task_name = request.data.get('task_name')
            print(task_name)
            tasks = []
            for name in task_name:
                tasks.append(Task.objects.filter(task__icontains=name))
            print(tasks)
            for task in tasks:
                # Only delete tasks of your own
                if task.first().account.id == account.id:
                    task.first().delete()
                else:
                    print("Task with id ", task.first().id, "can't be deleted by you!!!")
        return Response({"message": "delete task successfully"}, status=status.HTTP_200_OK)

    # deactivate user
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        try:
            account = self.get_object()
        except Http404:
            return Response("Account not found!", status=status.HTTP_404_NOT_FOUND)
        else:
            if account.role.name != 'admin':
                return Response("This account is not allowed to use this feature!", status=status.HTTP_403_FORBIDDEN)
            else:
                account_id = request.data.get("id")
                account = Account.objects.get(id=account_id)
                if account is not None:
                    account.is_active = False
                    account.save()
                return Response(self.serializer_class(account).data, status=status.HTTP_200_OK)

    # activate user
    @action(detail=True, methods=['post'])
    def activate(self, request, pk):
        try:
            account = self.get_object()
        except Http404:
            return Response("Account not found!", status=status.HTTP_404_NOT_FOUND)
        else:
            if account.role.name != 'admin':
                return Response("This account is not allowed to use this feature!", status=status.HTTP_403_FORBIDDEN)
            else:
                account_id = request.data.get("id")
                account = Account.objects.get(id=account_id)
                if account is not None:
                    account.is_active = True
                    account.save()
                return Response(self.serializer_class(account).data, status=status.HTTP_200_OK)
