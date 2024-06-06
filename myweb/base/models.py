# base/models.py
from django.db import models
from datetime import date

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    scheduled_date = models.DateField(default=date.today)  # Add this field

    def __str__(self):
        return self.title


