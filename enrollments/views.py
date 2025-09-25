from rest_framework import generics
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentListCreateAPI(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class EnrollmentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
