from rest_framework import serializers
from .models import State, Site, Shift, Task, Machinery, TaskStatus, TaskReport, ReasonForDelay, ShiftSummary

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    machinery = MachinerySerializer(many=True)  # Include machinery in task response

    class Meta:
        model = Task
        fields = ['id', 'name', 'machinery']

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReport
        fields = '__all__'

    def validate_machinery_used(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("machinery_used must be a list of text values.")
        return value


class ReasonForDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonForDelay
        fields = '__all__'

class ShiftSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftSummary
        fields = '__all__'
