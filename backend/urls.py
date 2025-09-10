# backend/urls.py

# ...existing code...
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api, name='test_api'),
    path('job-roles/', views.JobRoleListAPIView.as_view(), name='job-roles'),
    path('sessions/', views.InterviewSessionListCreateAPIView.as_view(), name='sessions'),
    path('generate-question/', views.generate_question, name='generate-question'),
    path('evaluate-answer/', views.evaluate_answer_view, name='evaluate-answer'),
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),  # <-- Add this line
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('test/', views.test_api, name='test_api'),
#     path('job-roles/', views.JobRoleListAPIView.as_view(), name='job-roles'), # Added trailing slash
#     path('sessions/', views.InterviewSessionListCreateAPIView.as_view(), name='sessions'),
#     path('generate-question/', views.generate_question, name='generate-question'),
#     path('evaluate-answer/', views.evaluate_answer_view, name='evaluate-answer'),
# ]