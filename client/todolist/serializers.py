from rest_framework import serializers
from .models import Task, TaskIncompleteReport, Site, TaskCompleteReport, PersonAttendaceRecord, PlantAttendance, PersonOnSite, PlantOnSite

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskIncompleteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskIncompleteReport
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Site
        fields = '__all__'

class TaskCompleteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompleteReport
        fields = '__all__'
        
        
class PersonOnSiteNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonOnSite
        fields = '__all__'
        
class PlantOnSiteNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantOnSite
        fields = '__all__'
    
        
class PersonOnSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonAttendaceRecord
        fields = '__all__'
    
class PlantOnSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantAttendance
        fields = '__all__'