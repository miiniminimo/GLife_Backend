# organizations/models.py
from django.db import models
from django.contrib.auth.hashers import make_password

class Company(models.Model):
    name = models.CharField(max_length=255)
    biz_no = models.CharField(max_length=20, unique=True)  # 사업자등록번호
    password = models.CharField(max_length=128)  # 해싱된 비밀번호
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 비밀번호 해싱 (새로 저장될 때만)
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.biz_no})"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    emp_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        unique_together = ("company", "emp_no")

    def __str__(self):
        return f"{self.emp_no} - {self.name}"
