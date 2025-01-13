from rest_framework import serializers
from .models import Task, TaskIncompleteReport, Site

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
