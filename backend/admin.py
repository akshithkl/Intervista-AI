from django.contrib import admin
from .models import JobRole, UserProfile, Roadmap, InterviewSession

# Register your models here.
@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'years_of_experience')
    list_filter = ('target_role', 'years_of_experience')
    search_fields = ('user__username', 'user__email')

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'job_role', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'job_role', 'created_at')
    search_fields = ('title', 'user__username')

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'job_role', 'created_at')
    list_filter = ('job_role', 'created_at')
    search_fields = ('title', 'user__username')
