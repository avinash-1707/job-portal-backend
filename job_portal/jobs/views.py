import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from .models import Company, JobPost, Applicant

@csrf_exempt
@require_http_methods(["POST"])
def create_company(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'location', 'description']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return JsonResponse({
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Create company
        company = Company.objects.create(
            name=data['name'].strip(),
            location=data['location'].strip(),
            description=data['description'].strip()
        )
        
        return JsonResponse({
            'message': 'Company created successfully',
            'company': {
                'id': company.id,
                'name': company.name,
                'location': company.location,
                'description': company.description,
                'created_at': company.created_at.isoformat()
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def post_job(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['company_id', 'title', 'description', 'salary', 'location']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Validate company exists
        try:
            company = Company.objects.get(id=data['company_id'])
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
        
        # Validate salary is positive integer
        try:
            salary = int(data['salary'])
            if salary < 0:
                return JsonResponse({'error': 'Salary must be positive'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid salary format'}, status=400)
        
        # Create job post
        job_post = JobPost.objects.create(
            company=company,
            title=data['title'].strip(),
            description=data['description'].strip(),
            salary=salary,
            location=data['location'].strip()
        )
        
        return JsonResponse({
            'message': 'Job posted successfully',
            'job': {
                'id': job_post.id,
                'company': company.name,
                'title': job_post.title,
                'description': job_post.description,
                'salary': job_post.salary,
                'location': job_post.location,
                'created_at': job_post.created_at.isoformat()
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_jobs(request):
    try:
        jobs = JobPost.objects.select_related('company').all().order_by('-created_at')
        
        job_list = []
        for job in jobs:
            job_list.append({
                'id': job.id,
                'title': job.title,
                'description': job.description,
                'salary': job.salary,
                'location': job.location,
                'company': {
                    'id': job.company.id,
                    'name': job.company.name,
                    'location': job.company.location
                },
                'created_at': job.created_at.isoformat()
            })
        
        return JsonResponse({
            'jobs': job_list,
            'total_jobs': len(job_list)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def apply_job(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'email', 'resume_link', 'job_id']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return JsonResponse({
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Validate job exists
        try:
            job = JobPost.objects.get(id=data['job_id'])
        except JobPost.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
        
        # Check if applicant already applied for this job
        existing_application = Applicant.objects.filter(
            email=data['email'].strip(),
            job=job
        ).first()
        
        if existing_application:
            return JsonResponse({
                'error': 'You have already applied for this job'
            }, status=400)
        
        # Create applicant
        applicant = Applicant.objects.create(
            name=data['name'].strip(),
            email=data['email'].strip(),
            resume_link=data['resume_link'].strip(),
            job=job
        )
        
        return JsonResponse({
            'message': 'Application submitted successfully',
            'application': {
                'id': applicant.id,
                'name': applicant.name,
                'email': applicant.email,
                'resume_link': applicant.resume_link,
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company.name
                },
                'applied_at': applicant.applied_at.isoformat()
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_applicants(request, job_id):
    try:
        # Validate job exists
        try:
            job = JobPost.objects.get(id=job_id)
        except JobPost.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
        
        applicants = Applicant.objects.filter(job=job).order_by('-applied_at')
        
        applicant_list = []
        for applicant in applicants:
            applicant_list.append({
                'id': applicant.id,
                'name': applicant.name,
                'email': applicant.email,
                'resume_link': applicant.resume_link,
                'applied_at': applicant.applied_at.isoformat()
            })
        
        return JsonResponse({
            'job': {
                'id': job.id,
                'title': job.title,
                'company': job.company.name
            },
            'applicants': applicant_list,
            'total_applicants': len(applicant_list)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)