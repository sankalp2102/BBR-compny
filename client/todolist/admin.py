from django.contrib import admin
from .models import Task, Site
# Register your models here.
#admin.site.register(TaskIncompleteReport)
admin.site.register(Task)
admin.site.register(Site)