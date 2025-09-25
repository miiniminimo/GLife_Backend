# organizations/serializers.py
from rest_framework import serializers
from .models import Company, Employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "biz_no", "created_at"]


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "biz_no", "password"]

    def create(self, validated_data):
        return Company.objects.create(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "emp_no", "name", "dept", "phone", "email", "company"]
        read_only_fields = ["company"]
