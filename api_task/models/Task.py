from django.db import models

from api_account.models import Account


class Task(models.Model):
    class Meta:
        db_table = 'task'

    task = models.CharField(max_length=200)
    deadline = models.DateTimeField(null=True)
    is_done = models.BooleanField(default=False)
    note = models.CharField(max_length=200, null=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="tasks")
