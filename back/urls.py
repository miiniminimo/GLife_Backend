"""
URL configuration for back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/organizations/", include("organizations.urls")),  # ✅ 이 줄 추가
    path("api/courses/", include("courses.urls")),             # 나중에 courses 연결
    path("api/enrollments/", include("enrollments.urls")),     # 나중에 enrollments 연결
    path("api/ai/", include("ai.urls")),                       # 나중에 ai 연결
]
