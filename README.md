# 🚀 Django Job Portal Backend

A comprehensive job portal backend built with Django that allows companies to post jobs and applicants to apply for positions.

## 📋 Features

- **Company Management**: Create and manage company profiles
- **Job Posting**: Companies can post job openings with detailed descriptions
- **Job Applications**: Applicants can apply for jobs with resume links
- **Application Tracking**: View all applicants for specific jobs
- **RESTful API**: Clean JSON API endpoints for frontend integration
- **Admin Interface**: Django admin panel for easy management

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, easily configurable)
- **API**: Django JsonResponse (No DRF)
- **Authentication**: Django built-in (for admin)

## 📊 Database Models

### Company

- name (CharField)
- location (CharField)
- description (TextField)
- created_at (DateTimeField)

### JobPost

- company (ForeignKey to Company)
- title (CharField)
- description (TextField)
- salary (IntegerField)
- location (CharField)
- created_at (DateTimeField)

### Applicant

- name (CharField)
- email (EmailField)
- resume_link (URLField)
- job (ForeignKey to JobPost)
- applied_at (DateTimeField)

## 🔗 API Endpoints

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| POST   | `/api/create-company/`      | Create a new company     |
| POST   | `/api/post-job/`            | Create a new job posting |
| GET    | `/api/jobs/`                | Get all job postings     |
| POST   | `/api/apply/`               | Apply for a job          |
| GET    | `/api/applicants/<job_id>/` | Get applicants for a job |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/avinash-1707/job-portal-backend.git
   cd job_portal
   ```
2. **Run the migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate
    ```
3. **Run the server**
```bash
python manage.py run server
```
