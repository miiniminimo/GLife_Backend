from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, AllowAny
from django.contrib.auth.hashers import check_password
from django.conf import settings

import jwt, datetime

from .models import Company, Employee
from .serializers import (
    CompanyCreateSerializer,
    CompanySerializer,
    EmployeeSerializer,
)


# ✅ 회사 로그인 세션 권한
class IsCompanySession(BasePermission):
    def has_permission(self, request, view):
        return bool(request.session.get("company_id"))


# ✅ 회사 로그인 API (사업자등록번호 + 비밀번호)
class CompanyLoginAPI(APIView):
    """
    POST /api/organizations/login/
    {
      "biz_no": "1234567890",
      "password": "비밀번호"
    }
    """

    def post(self, request):
        biz_no = request.data.get("biz_no")
        password = request.data.get("password")

        try:
            company = Company.objects.get(biz_no=biz_no)
            if not check_password(password, company.password):
                return Response(
                    {"error": "비밀번호 불일치"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            payload = {
                "company_id": company.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            # 세션에도 저장 (회사 로그인 상태 유지)
            request.session["company_id"] = company.id

            return Response({"token": token}, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response(
                {"error": "존재하지 않는 회사"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ✅ 회사 CRUD
class CompanyViewSet(viewsets.ModelViewSet):
    """
    회사 회원가입 / 조회
    """

    queryset = Company.objects.all().order_by("-created_at", "-id")

    def get_permissions(self):
        if self.action == "create":  # 회원가입은 공개
            return [AllowAny()]
        return [IsCompanySession()]

    def get_serializer_class(self):
        return (
            CompanyCreateSerializer
            if self.action == "create"
            else CompanySerializer
        )


# ✅ 직원 CRUD
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    직원 CRUD + JSON 대량 업로드
    """

    permission_classes = [IsCompanySession]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        cid = self.request.session.get("company_id")
        return Employee.objects.select_related("company").filter(company_id=cid)

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request):
        """
        직원 JSON 대량 업로드
        요청 예시:
        {
          "employees": [
            {"emp_no":"E001","name":"홍길동","dept":"개발","phone":"010-1234-5678","email":"hong@test.com"},
            {"emp_no":"E002","name":"김철수","dept":"인사","phone":"010-2222-3333","email":"kim@test.com"}
          ]
        }
        """
        cid = request.session.get("company_id")
        if not cid:
            return Response({"detail": "Unauthorized"}, status=401)

        rows = request.data.get("employees", [])
        if not isinstance(rows, list):
            return Response(
                {"detail": "employees must be a list"}, status=400
            )

        created, updated = 0, 0
        for r in rows:
            emp_no = (r.get("emp_no") or "").strip()
            if not emp_no:
                continue

            defaults = {
                "name": r.get("name", "") or "",
                "dept": r.get("dept", "") or "",
                "phone": r.get("phone", "") or "",
                "email": r.get("email", "") or "",
            }

            obj, was_created = Employee.objects.update_or_create(
                company_id=cid, emp_no=emp_no, defaults=defaults
            )

            created += 1 if was_created else 0
            updated += 0 if was_created else 1

        return Response(
            {
                "ok": True,
                "created": created,
                "updated": updated,
                "count": len(rows),
            }
        )
