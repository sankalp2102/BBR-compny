from rest_framework import serializers
from .models import (State, Site, Task,
                     Machinery, TaskStatus,
                     TaskReport, ReasonForDelay,
                     ShiftSummary, Quantity,
                     Reconcilation, CustomUser)
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
        fields = ['id', 'name', 'time_from', 'time_to']

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
    site_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'site_ids']

    def create(self, validated_data):
        site_ids = validated_data.pop('site_ids', [])
        user = CustomUser.objects.create_user(**validated_data)

        # If the role is Technician, assign sites
        if user.role == 'Technician':
            sites = Site.objects.filter(id__in=site_ids)
            user.assigned_sites.set(sites)
        
        return user
    
class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = '__all__'
        
class ReconcilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconcilation
        fields = '__all__'