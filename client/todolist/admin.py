from django.contrib import admin
from .models import Task, Site, PersonAttendaceRecord, PlantAttendance, PlantOnSite, PersonOnSite
# Register your models here.
#admin.site.register(TaskIncompleteReport)
admin.site.register(Task)
admin.site.register(Site)
admin.site.register(PlantAttendance)
admin.site.register(PersonAttendaceRecord)
admin.site.register(PlantOnSite)
admin.site.register(PersonOnSite)