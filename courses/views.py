from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer

class CourseListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # JWT 토큰의 user(Company) 정보를 기반으로 강좌를 필터링합니다.
        return Course.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        # 강좌 생성 시, 요청한 user(Company) 소속으로 자동 설정합니다.
        serializer.save(company=self.request.user)


class CourseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # JWT 토큰의 user(Company) 정보를 기반으로 강좌를 필터링합니다.
        return Course.objects.filter(company=self.request.user)
