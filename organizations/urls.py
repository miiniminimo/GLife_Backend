from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, EmployeeViewSet, CompanyLoginAPI

# ✅ 라우터 등록 (ViewSet 기반)
router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    # 로그인 API
    path("login/", CompanyLoginAPI.as_view(), name="company-login"),

    # ViewSet 라우터 API
    path("", include(router.urls)),
]
