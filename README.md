# MAT633 Project Registration System

Prepared for Dr Zahari Bin Md Rodzi  
Semester March -- September 2026

## Features

- Student project registration form
- Group member details for 3 to 4 students
- Matrix number and class collection
- Abstract submission
- Duplicate checking by project title and group leader matrix number
- Admin dashboard with password
- Search and filter submissions
- Download CSV data

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Admin Password

Default password:

```text
mat633admin
```

Change this line in `app.py` before real deployment:

```python
ADMIN_PASSWORD = "mat633admin"
```

## Data Storage

Submissions are saved in:

```text
data/mat633_project_submissions.csv
```

## Deployment Notes

For Streamlit Community Cloud, GitHub deployment is simple. For safer institutional deployment, use a private server, institutional cloud, or managed deployment with login protection.
