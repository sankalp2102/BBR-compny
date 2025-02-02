from rest_framework import serializers
from .models import TaskIncompleteReport, TaskCompleteReport, PersonAttendaceRecord, PlantAttendance, Site, State, ShiftData


class TaskIncompleteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskIncompleteReport
        fields = '__all__'

class TaskCompleteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompleteReport
        fields = '__all__'  

class PersonOnSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonAttendaceRecord
        fields = '__all__'
    
class PlantOnSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantAttendance
        fields = '__all__'
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name', 'state']

class ShiftDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftData
        exclude = ['created_at']