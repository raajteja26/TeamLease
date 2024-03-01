from django.urls import path
from .views import employees_list
from .views import EmployeeList
from .views import upload,delete_all

urlpatterns = [
    path('employees/', employees_list, name='employees_list'),
    path('list-employees/', EmployeeList.as_view(), name='list_employees'),
    path("upload/",upload,name="upload"),
    path("delete_all/", delete_all,name="delete_all")
]
