from rest_framework import serializers
from .models import State, Site, Shift, Task, Machinery, TaskStatus, TaskReport, ReasonForDelay, ShiftSummary
from django.contrib.auth import get_user_model

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
    def to_representation(self, instance):
        """Ensure JSON fields return proper lists instead of strings."""
        data = super().to_representation(instance)

        # ✅ Ensure JSON fields are properly returned as lists
        json_fields = ["personnel_engaged", "machinery_used", "equipment_used", "personnel_idled", "equipment_idled"]
        for field in json_fields:
            if isinstance(data[field], str):  # If stored as a string, convert it back to JSON
                import json
                data[field] = json.loads(data[field])

        return data


class ReasonForDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonForDelay
        fields = '__all__'

class ShiftSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftSummary
        fields = '__all__'



User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user