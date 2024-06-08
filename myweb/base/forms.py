# forms.py
from django import forms
from .models import  Note, Task, Profile, Project



class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['name', 'lastname', 'about', 'phone_number', 'email']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile




class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'due_date']





