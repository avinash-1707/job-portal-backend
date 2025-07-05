from django.contrib import admin
from .models import Company, JobPost, Applicant

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'salary', 'location', 'created_at')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('created_at', 'company', 'location')

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_at')
    search_fields = ('name', 'email', 'job__title')
    list_filter = ('applied_at', 'job__company')