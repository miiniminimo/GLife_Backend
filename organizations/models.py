from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)  # 회사명
    biz_no = models.CharField(max_length=20, unique=True)  # 사업자등록번호 (로그인 ID 역할)
    password = models.CharField(max_length=128)  # 비밀번호 (hash 권장)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.biz_no})"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    emp_no = models.CharField(max_length=20, unique=True)  # 사번
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100, blank=True, null=True)  # 부서
    position = models.CharField(max_length=100, blank=True, null=True)  # 직급
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.emp_no})"
