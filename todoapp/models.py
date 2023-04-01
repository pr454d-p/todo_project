from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.title