# forms.py
from django import forms
from .models import Task
from .models import Plan


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'due_date']

