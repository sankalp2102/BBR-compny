from rest_framework import serializers
from .models import State, Site, ShiftData, TaskStatus, IncompleteTaskEvidence, Headcount

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
        
        
class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'description', 'status', 'created_at']

class IncompleteTaskEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncompleteTaskEvidence
        fields = ['image', 'latitude', 'longitude', 'notes']

class TaskCreateSerializer(serializers.Serializer):
    shift_data_id = serializers.IntegerField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=['completed', 'incomplete'])
    image = serializers.ImageField(required=False)
    latitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    notes = serializers.CharField(required=False, allow_blank=True)
    
class HeadcountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headcount
        fields = ['id', 'person_name', 'count', 'date', 'shift']

class HeadcountCreateSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
    person_name = serializers.CharField(max_length=100)
    count = serializers.IntegerField(min_value=1)
    date = serializers.DateField(required=False)
    shift = serializers.IntegerField(required=False)