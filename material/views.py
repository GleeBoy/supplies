from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, filters
from material.serializers import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, FileResponse
from django.contrib import auth
import json, os
from rest_framework.pagination import PageNumberPagination
# Create your views here.


def delete_cookie(response):
    response.delete_cookie('username')
    response.delete_cookie('id')
    response.delete_cookie('permissions')


# @require_http_methods(['GET', 'POST'])
@ensure_csrf_cookie
def login(request):
    """
    登录
    :param request:
    :return:
    """
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    if request.method == 'GET':
        if request.user.is_authenticated:
            response = JsonResponse({'status': True})
            delete_cookie(response)
        else:
            response = JsonResponse({'status': False})
    else:
        UN = request.POST.get('UN', None)
        PW = request.POST.get('PW', None)
        try:
            user = auth.authenticate(request, username=UN, password=PW)
            if user is not None:
                auth.login(request=request, user=user)
                response = JsonResponse({'status': True})
                response.set_cookie('username', user.username)
                response.set_cookie('id', user.id)
                groups = user.groups.all()
                if '管理员' in [group.name for group in groups]:
                    response.set_cookie('permissions', True)
            else:
                response = JsonResponse({'status': False})
        except Exception as e:
            print(e)
            response = HttpResponse(json.dumps({'status': False, 'msg': '登录方式暂不支持'}, ensure_ascii=False),
                                    content_type='application/json')
    return response


@require_http_methods(['GET'])
def logout(request):
    """
    登出
    :param request:
    :return:
    """
    auth.logout(request)
    response = JsonResponse({'status': False})
    delete_cookie(response)
    return response


def handle_uploaded_file(fpath, f):
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    fpath = fpath + f.name
    with open(fpath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fpath


class MaterialInfoViewSet(viewsets.ModelViewSet):
    queryset = MaterialInfo.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['item_code', 'item_name', 'describe', 'firm_code', 'firm_name', 'remark']
    # permission_classes = [MopLevel1MenuPermission]


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SuperclassViewSet(viewsets.ModelViewSet):
    queryset = Superclass.objects.all()
    serializer_class = SuperclassSerializer
    pagination_class = LargeResultsSetPagination


class SubclassViewSet(viewsets.ModelViewSet):
    queryset = Subclass.objects.all()
    serializer_class = SubclassSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['superclass__code']
    pagination_class = LargeResultsSetPagination


def middle_str(request):
    superClass = request.GET.get('superClass')
    subClass = request.GET.get('subClass')
    code = superClass + subClass
    mat = MaterialInfo.objects.filter(item_code__startswith=code)
    if mat.exists():
        item_code = mat.order_by('-item_code').first().item_code
        num = int(item_code[5:-3]) + 1
    else:
        num = 1
    num_str = str(num).zfill(5)
    return JsonResponse({'results': num_str})


def check_firm(request):
    firm_code = request.GET.get('firm_code')
    firm_name = request.GET.get('firm_name')
    mater = MaterialInfo.objects.filter(firm_code=firm_code, firm_name=firm_name)
    if mater.exists():
        results = 'yes'
    else:
        results = 'no'
    return JsonResponse({'results': results})


def test(request):
    print(request)
    return JsonResponse({})


def get_sub(request):
    sub = Subclass.objects.filter(superclass__name=request.GET.get('superName'))
    if sub.exists():
        sub_code = sub.order_by('-code').first().code
        next_sub_code = str(int(sub_code) + 1).zfill(2)
    else:
        next_sub_code = '01'
    return JsonResponse({'sub_code': next_sub_code})


def check_super_code(request):
    if Superclass.objects.filter(code=request.GET.get('code')).exists():
        return JsonResponse({'results': 'yes'})
    else:
        return JsonResponse({'results': 'no'})


def check_super_name(request):
    if Superclass.objects.filter(name=request.GET.get('name')).exists():
        return JsonResponse({'results': 'yes'})
    else:
        return JsonResponse({'results': 'no'})


def check_sub_name(request):
    if Subclass.objects.filter(superclass__name=request.GET.get('super_name'), name=request.GET.get('name')).exists():
        return JsonResponse({'results': 'yes'})
    else:
        return JsonResponse({'results': 'no'})
