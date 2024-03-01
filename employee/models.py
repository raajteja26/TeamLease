from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

class FileUpload(models.Model):
    file = models.FileField(upload_to="./files")

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    email = models.EmailField(validators=[EmailValidator(message="Please enter a valid email address.")])
    mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{10,15}$', message="Please enter a valid mobile number.")])
    date_of_join = models.DateField()
    
    def __str__(self):
        return self.name
