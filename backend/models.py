from django.db import models

# Create your models here.
# backend/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class JobRole(models.Model):
    """Stores different job roles like 'Software Engineer', 'Data Scientist'"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    """Extends the default User model to store user-specific data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Link profile to a desired job role
    target_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True, null=True)  # Could be a simple comma-separated list for now
    years_of_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Roadmap(models.Model):
    """Stores a personalized preparation plan for a user and a specific job role"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # e.g., "30-Day Prep Plan for Backend Engineers"
    # We can store the generated plan as JSON in a TextField
    plan_data = models.JSONField(default=dict)  # Structure: { "week_1": ["Topic A", "Topic B"], ...}
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'job_role')  # One roadmap per user per role

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class InterviewSession(models.Model):
    """Stores a Q&A session with the AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="Untitled Session")
    # Store the conversation history with the AI
    conversation_history = models.JSONField(default=list)  # List of {"role": "user"/"assistant", "content": "text"}
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)  # Overall feedback generated at the end

    def __str__(self):
        return f"Session: {self.title} ({self.user.username})"

# (We'll add a model for scraped jobs later)