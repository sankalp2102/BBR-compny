from django.contrib import admin
from .models import Site, State, ShiftData, Headcount
# Register your models here.
admin.site.register(State)
admin.site.register(Site)
admin.site.register(ShiftData)
admin.site.register(Headcount)