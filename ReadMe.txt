
# Installation Instructions:
1. Make sure you have Python,Django installed on your system.

2. Install the required packages by running the following command:
   pip install -r requirements.txt

# Database Migration:
3. Make migrations for database changes:
   python manage.py makemigrations

4. Apply the migrations to the database:
   python manage.py migrate

# Running the Server:
5. Start the Django development server:
   python manage.py runserver

# Running Celery Worker and Flower Monitoring:
6. Run Celery Flower for monitoring tasks:
   python -m celery -A employee_project flower

7. Run Celery Worker for executing tasks:
   python -m celery -A employee_project worker --pool=solo -l info

# Accessing the API:
8. Access the API for employees' data at:
   http://127.0.0.1:8000/api/employees/

# Note:
- Ensure that you have configured your database settings in settings.py file.
- Make sure to have appropriate permissions and environment setup for running the commands.
