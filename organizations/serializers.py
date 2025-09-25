from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Company

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
