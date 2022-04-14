from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    manager: int = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task: str = models.CharField(max_length=255)
    done: bool = models.BooleanField(default=False)

    def __str__(self):
        return f'task: {self.task} - done: {str(self.done)} '
