from django.urls import path
from .views import CompanyLoginAPI, EmployeeListCreateAPI, EmployeeDetailAPI

urlpatterns = [
    path("auth/login/", CompanyLoginAPI.as_view(), name="company_login"),
    path("employees/", EmployeeListCreateAPI.as_view(), name="employee_list_create"),
    path("employees/<int:pk>/", EmployeeDetailAPI.as_view(), name="employee_detail"),
]
