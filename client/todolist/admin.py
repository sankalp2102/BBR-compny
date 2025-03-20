from django.contrib import admin
from .models import (State, Site, Shift, 
                     Task, Machinery, TaskStatus,
                     TaskReport, ReasonForDelay,
                     ShiftSummary, CustomUser)

admin.site.register(State)
admin.site.register(Site)
admin.site.register(Shift)
admin.site.register(Task)
admin.site.register(Machinery)
admin.site.register(TaskStatus)
admin.site.register(TaskReport)
admin.site.register(ReasonForDelay)
admin.site.register(ShiftSummary)
admin.site.register(CustomUser)
