from django.urls import path
from . import views

urlpatterns = [
    path('api/create-company/', views.create_company, name='create_company'),
    path('api/post-job/', views.post_job, name='post_job'),
    path('api/jobs/', views.get_jobs, name='get_jobs'),
    path('api/apply/', views.apply_job, name='apply_job'),
    path('api/applicants/<str:job_id>/', views.get_applicants, name='get_applicants'),
]