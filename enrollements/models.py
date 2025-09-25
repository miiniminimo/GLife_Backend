from django.db import models
from organizations.models import Employee
from courses.models import Course

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("enrolled", "수강"),
        ("pending", "미수강"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ("employee", "course")  # 같은 과정 중복 등록 방지

    def __str__(self):
        return f"{self.employee.name} - {self.course.title} ({self.status})"
