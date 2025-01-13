from rest_framework import serializers
from .models import Task, TaskIncompleteReport, Site, TaskCompleteReport, MachineAtteandance

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
        
class MachineAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineAtteandance
        fields = '__all__'