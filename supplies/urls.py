"""supplies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from material.views import *
from rest_framework.routers import DefaultRouter
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

router = DefaultRouter()
router.register(r'materialinfo', MaterialInfoViewSet, basename='materialinfo')
router.register(r'superclass', SuperclassViewSet, basename='superclass')
router.register(r'subclass', SubclassViewSet, basename='subclass')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('manage/', include(router.urls)),
    path('middle_str/', middle_str),
    path('check_firm/', check_firm),
    path('test/', test),
    path('get_sub/', get_sub),
    path('check_super_code/', check_super_code),
    path('check_super_name/', check_super_name),
    path('check_sub_name/', check_sub_name),
    re_path(r"^media/img/(?P<path>.*)", serve, {"document_root": settings.UPLOAD_IMG}),
    re_path(r"^media/specification/(?P<path>.*)", serve, {"document_root": settings.UPLOAD_SPE}),
    re_path('^.*$', TemplateView.as_view(template_name='index.html'), name='vue_app'),
]
