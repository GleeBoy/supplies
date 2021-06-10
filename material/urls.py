from django.urls import path, include, re_path
from material.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'materialinfo', MaterialInfoViewSet, basename='materialinfo')
router.register(r'superclass', SuperclassViewSet, basename='superclass')
router.register(r'subclass', SubclassViewSet, basename='subclass')
router.register(r'mediaimg', MediaImgViewSet, basename='mediaimg')
urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('manage/', include(router.urls)),
    path('middle_str/', middle_str),
    path('check_firm/', check_firm),
    path('test/', test),
    path('get_sub/', get_sub),
    path('check_super_code/', check_super_code),
    path('check_super_name/', check_super_name),
    path('check_sub_name/', check_sub_name)
]