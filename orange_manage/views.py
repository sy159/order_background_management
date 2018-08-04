from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Sum, Q, F
from orange_manage import models
from .tool import area_data as area
from .tool import login_validation as val
from .tool import produce_key as key
import json, hashlib


# Create your views here.

@csrf_protect
def login(request):
    '''
    登陆跳转
    '''
    if request.method == 'POST':
        get_ip = request.META['REMOTE_ADDR']
        last_time = timezone.now()
        get_name = request.POST.get('account', None)
        get_pwd = request.POST.get('pwd', None)
        hash_key = hashlib.sha256()
        hash_key.update(get_pwd.encode())
        get_pwd = hash_key.hexdigest()
        get_verifycode = request.POST.get('verifycode')
        get_name_obj = models.Admin.objects.filter(account=get_name).first()
        if get_name_obj:  # 判断用户是否存在
            if get_name_obj.pwd == get_pwd:  # 判断密码是否正确
                judge = models.Admin.objects.filter(account=get_name).values_list('admin_key').first()[0]
                if judge:  # 判断是否第一次登陆
                    if val.validation(judge, get_verifycode):  # 判断验证码是否正确
                        request.session['user'] = get_name
                        request.session['judge'] = True
                        models.Admin.objects.filter(account=get_name).update(last_time=last_time, last_ip=get_ip,
                                                                             login_count=F('login_count') + 1)
                        return redirect('/admin/index/')
                    else:
                        return render(request, 'login.html', {'error_msg': '验证码错误'})
                else:
                    request.session['user'] = get_name
                    request.session['judge'] = True
                    models.Admin.objects.filter(account=get_name).update(last_time=last_time, last_ip=get_ip,
                                                                         login_count=F('login_count') + 1)
                    return redirect('/admin/bind_account/')
            return render(request, 'login.html', {'error_msg': '密码错误'})
        return render(request, 'login.html', {'error_msg': '该用户不存在'})
    else:
        return render(request, 'login.html', {'error_msg': ''})


def logout(request):
    '''
    注销
    '''
    request.session.clear()
    return redirect('/admin/login/')


def bind_account(request):
    '''
    两步验证
    '''
    if request.method == "GET":
        if request.GET.get('erro'):
            erro = '输入的校验错误，请重新绑定'
        else:
            erro = ''
        account = request.session.get('user')
        keys = key.login_key()
        qr_code = 'otpauth://totp/' + account + '?secret=' + keys
        return render(request, 'bind_account.html', {'account': account, 'key': keys, "code": qr_code, 'erro': erro})
    elif request.method == "POST":
        get_account = request.session.get('user')
        get_key = request.POST.get('key')
        get_code = request.POST.get('check_code')
        if val.validation(get_key, get_code):
            models.Admin.objects.filter(account=get_account).update(admin_key=get_key)
            return redirect('/admin/index/')
        else:
            return redirect('/admin/bind_account/?erro=1')


def index(request):
    get_account = request.session.get('user')
    obj = models.Admin.objects.filter(account=get_account).first()
    menus_list = json.loads(obj.menus)
    data_list = []
    for i in menus_list:
        for key, value in i.items():
            index_obj = models.Menu.objects.filter(id=key).first()
            index_name = index_obj.field_function_name
            data_dict = {}
            child_list = []
            for j in value:
                child_dict = {}
                child_obj = models.Menu.objects.filter(id=j).first()
                child_name = child_obj.field_function_name
                child_url = child_obj.field_function_url
                child_dict['child_url'] = child_url
                child_dict['child_name'] = child_name
                child_list.append(child_dict)
            data_dict[index_name] = child_list
        data_list.append(data_dict)
    return render(request, 'index.html', {'data': data_list, 'account': get_account, 'identity': obj.level})


def account_unique(request):
    get_account = request.GET.get('account')
    if models.Admin.objects.filter(account=get_account):
        return JsonResponse({'state': 1})
    else:
        return JsonResponse({'state': 0})
