# serializers.py
from rest_framework import serializers
from .models import Employee, FileUpload

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        exclude = ('file')