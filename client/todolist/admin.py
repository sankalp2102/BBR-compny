from django.contrib import admin
from .models import PersonAttendaceRecord, PlantAttendance, TaskIncompleteReport, ShiftData, Site, State
# Register your models here.
admin.site.register(State)
admin.site.register(Site)
admin.site.register(ShiftData)
admin.site.register(TaskIncompleteReport)
admin.site.register(PlantAttendance)
admin.site.register(PersonAttendaceRecord)