from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "emp_no", "name", "dept", "phone", "email", "company"]
        # company 필드는 요청 데이터가 아닌, 로그인 정보(JWT)를 통해 자동으로 설정되므로 읽기 전용으로 지정
        read_only_fields = ["id", "company"]


class CompanyTokenObtainPairSerializer(serializers.Serializer):
    biz_no = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        biz_no = attrs.get("biz_no")
        password = attrs.get("password")

        try:
            company = Company.objects.get(biz_no=biz_no)

        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid business number or password")

        if not company.check_password(password):
            raise serializers.ValidationError("Invalid business number or password")

        # 👇 JWT 발급 (SimpleJWT 직접 사용)
        refresh = RefreshToken.for_user(company)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "company": {
                "biz_no": company.biz_no,
                "name": company.name,
            }
        }
