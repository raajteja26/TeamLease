from django.http import JsonResponse
from celery import shared_task
import csv
from .models import Employee
from django.shortcuts import render
from elasticsearch import Elasticsearch
from .models import Employee
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
import csv
from .models import Employee,FileUpload
from .serializers import  FileUploadSerializer,EmployeeSerializer
from rest_framework.views import APIView
import pandas as pd
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
from celery.result import AsyncResult
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    

@shared_task
def create_data(file_path):
    df = pd.read_csv(file_path, delimiter=",")
    batch_size = 100
    total_records = len(df)
    num_batches = (total_records + batch_size - 1) // batch_size

    failed_records = []

    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, total_records)
        batch_df = df.iloc[start_idx:end_idx]

        batch_failed_records = []

        for index, row in batch_df.iterrows():
            errors = []
            try:
                validate_email(row['email'])
            except ValidationError as e:
                errors.append(f"Invalid email: {e}")
            mobile_number = str(row['mobile'])
            if not (10 <= len(mobile_number) <= 15):
                errors.append("Mobile number must be between 10 and 15 digits")
            try:
                datetime.datetime.strptime(row['date_of_join'], '%Y-%m-%d')
            except ValueError:
                errors.append("Invalid date format. Date must be in YYYY-MM-DD format")

            if errors:
                batch_failed_records.append({'record': row['name'], 'errors': errors})
                continue

            Employee.objects.create(
                name=row['name'],
                email=row['email'],
                mobile=mobile_number,
                date_of_join=row['date_of_join'],
            )

        failed_records.extend(batch_failed_records)

    return failed_records

def upload(request):
    failed_records = []

    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            obj = FileUpload.objects.create(file=file)
            async_result = create_data.delay(obj.file.path)
            messages.success(request, "File uploaded successfully!")
            result = AsyncResult(async_result.id)
            if result.ready():
                failed_records = result.get()
                print(failed_records,"FAILED")
        else:
            messages.error(request, "No file provided")
    return render(request, "upload.html", {'failed_records': failed_records})


@csrf_exempt
def delete_all(request):
    if request.method == 'DELETE':
        Employee.objects.all().delete()
        return JsonResponse({'message': 'All employees deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def employees_list(request):
    search_query = request.GET.get('search')
    if search_query:
        employees = Employee.objects.filter(Q(mobile=search_query))
    else:
        employees = Employee.objects.all()

    paginator = Paginator(employees, 100)
    page_number = request.GET.get('page')
    try:
        employees = paginator.page(page_number)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee_list.html', {'employees': employees})


class EmployeeList(APIView):
    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)



