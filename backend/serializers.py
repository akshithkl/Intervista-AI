# backend/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobRole, UserProfile, Roadmap, InterviewSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    target_role = JobRoleSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class RoadmapSerializer(serializers.ModelSerializer):
    job_role = JobRoleSerializer(read_only=True)

    class Meta:
        model = Roadmap
        fields = '__all__'

class InterviewSessionSerializer(serializers.ModelSerializer):
    job_role = JobRoleSerializer(read_only=True)

    class Meta:
        model = InterviewSession
        fields = '__all__'