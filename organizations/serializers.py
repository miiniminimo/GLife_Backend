from rest_framework import serializers
from .models import Company, Employee

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "biz_no", "created_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "emp_no", "name", "dept", "position", "company", "created_at"]
