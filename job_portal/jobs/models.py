from django.db import models
from django.core.validators import EmailValidator
import uuid

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class JobPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class Applicant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    resume_link = models.URLField()
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applicants')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"