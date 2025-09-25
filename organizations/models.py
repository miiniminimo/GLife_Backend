from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Company(models.Model):
    """
    사업자(회사) 계정 모델
    - biz_no: 로그인 ID로 사용 (사업자번호)
    - password: Django 해싱 방식 저장 (pbkdf2_sha256 등)
    """
    name = models.CharField(max_length=255)
    biz_no = models.CharField(max_length=20, unique=True)  # 사업자등록번호 (로그인 ID)
    password = models.CharField(max_length=128)  # 해싱된 비밀번호
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """비밀번호를 해싱하여 저장"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """입력된 비밀번호와 저장된 해시 비교"""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """새 비밀번호일 경우 자동 해싱 후 저장"""
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.biz_no})"


class Employee(models.Model):
    """
    회사에 속한 직원 정보
    """
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
