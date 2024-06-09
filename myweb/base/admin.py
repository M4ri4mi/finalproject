from django.contrib import admin
from .models import Profile, Note, Task, Project, Tag

admin.site.register(Profile)
admin.site.register(Note)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Tag)
