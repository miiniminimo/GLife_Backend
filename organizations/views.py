from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
import jwt, datetime
from django.conf import settings


class CompanyLoginAPI(APIView):
    """
    회사 로그인: 사업자등록번호 + 비밀번호
    """
    def post(self, request):
        biz_no = request.data.get("biz_no")
        password = request.data.get("password")

        try:
            company = Company.objects.get(biz_no=biz_no)
            if not check_password(password, company.password):
                return Response({"error": "비밀번호 불일치"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = {
                "company_id": company.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            return Response({"token": token}, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response({"error": "존재하지 않는 회사"}, status=status.HTTP_404_NOT_FOUND)


class EmployeeListCreateAPI(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
