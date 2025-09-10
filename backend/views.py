from django.shortcuts import render

# backend/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from .models import JobRole, InterviewSession, Roadmap
from .serializers import JobRoleSerializer, InterviewSessionSerializer, RoadmapSerializer
from .services.ai_service import generate_interview_question, evaluate_answer  # Add this import

# Add the missing test_api function
@api_view(['GET'])
def test_api(request):
    """Simple test endpoint to verify the API is working"""
    data = {
        "message": "Welcome to the Intervista API! 🚀",
        "status": "success",
        "endpoints": {
            "test": "/api/test/",
            "job_roles": "/api/job-roles/",
            "sessions": "/api/sessions/",
            "generate_question": "/api/generate-question/",
            "evaluate_answer": "/api/evaluate-answer/"
        }
    }
    return Response(data)

# AI Views - ADD THESE NEW VIEWS
@api_view(['POST'])
def generate_question(request):
    """Generate an interview question using AI"""
    job_role = request.data.get('job_role', 'Software Engineer')
    experience_level = request.data.get('experience_level', 'beginner')
    
    question = generate_interview_question(job_role, experience_level)
    
    return Response({
        'question': question,
        'job_role': job_role,
        'experience_level': experience_level
    })

@api_view(['POST'])
def evaluate_answer_view(request):
    """Evaluate user's answer using AI"""
    question = request.data.get('question')
    user_answer = request.data.get('answer')
    job_role = request.data.get('job_role', 'Software Engineer')
    
    if not question or not user_answer:
        return Response(
            {'error': 'Question and answer are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    feedback = evaluate_answer(question, user_answer, job_role)
    
    return Response({
        'feedback': feedback,
        'question': question,
        'job_role': job_role
    })

class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object to access it."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class JobRoleListAPIView(APIView):
    """Get a list of all available job roles to choose from"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roles = JobRole.objects.all()
        serializer = JobRoleSerializer(roles, many=True)
        return Response(serializer.data)

class InterviewSessionListCreateAPIView(APIView):
    """List user's sessions or create a new one."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(user=request.user)
        serializer = InterviewSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InterviewSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.models import User

class RegisterUserAPIView(APIView):
    """API endpoint for registering a new user."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)