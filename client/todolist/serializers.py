from rest_framework import serializers
from .models import State, Site, ShiftData, TaskStatus, IncompleteTaskEvidence, Headcount
from django.contrib.auth.models import User

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

class TaskStatusResponseSerializer(serializers.ModelSerializer):
    evidence = IncompleteTaskEvidenceSerializer(source='incompletetaskevidence', read_only=True)
    
    class Meta:
        model = TaskStatus
        fields = ['id', 'description', 'status', 'created_at', 'evidence']

class TaskCreateSerializer(serializers.Serializer):
    shift_data_id = serializers.IntegerField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=['completed', 'incomplete'])
    image = serializers.ImageField(required=False)
    latitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data.get('status') == 'incomplete':
            if not all(field in data for field in ['image', 'latitude', 'longitude']):
                raise serializers.ValidationError(
                    "Image, latitude, and longitude are required for incomplete tasks"
                )
        return data
    
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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)