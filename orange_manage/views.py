import json
import time

from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from orange_manage import models
from orange_manage.utils.image_upload import UploadImg
from .utils import login_validation as val
from .utils import produce_key as key
from .utils.password_encryption import pwd_encrypted


# Create your views here.
def home(request):
    return HttpResponseRedirect('/admin/index')


@csrf_protect
def login(request):
    """登陆跳转"""
    if request.method == 'POST':
        get_ip = request.META['REMOTE_ADDR']
        last_time = timezone.now()
        get_name = request.POST.get('account')
        get_pwd = pwd_encrypted(request.POST.get('pwd'))
        get_verifycode = request.POST.get('verifycode')
        get_name_obj = models.Admin.objects.filter(account=get_name).first()
        if get_name_obj:  # 判断用户是否存在
            if get_name_obj.pwd == get_pwd:  # 判断密码是否正确
                admin = models.Admin.objects.filter(account=get_name).first()
                if admin.admin_key:  # 判断是否第一次登陆
                    if val.validation(admin.admin_key, get_verifycode):  # 判断验证码是否正确
                        request.session['user'] = get_name
                        request.session['judge'] = True
                        models.Admin.objects.filter(account=get_name).update(last_time=last_time, last_ip=get_ip,
                                                                             login_count=F('login_count') + 1)
                        admin = models.Admin.objects.filter(account=get_name).first()
                        return redirect('/admin/index')
                    else:
                        return render(request, 'login.html', {'error_msg': '验证码错误'})
                else:
                    request.session['user'] = get_name
                    request.session['judge'] = True
                    models.Admin.objects.filter(account=get_name).update(last_time=last_time, last_ip=get_ip,
                                                                         login_count=F('login_count') + 1)
                    return redirect('/admin/bind_account')
            return render(request, 'login.html', {'error_msg': '密码错误'})
        return render(request, 'login.html', {'error_msg': '该用户不存在'})
    else:
        return render(request, 'login.html', {'error_msg': ''})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/admin/login')


def bind_account(request):
    """两步验证"""
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
            return redirect('/admin/index')
        else:
            return redirect('/admin/bind_account?erro=1')


def index(request):
    menus_list = json.loads(request.operator_menus)
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
    account_info = {
        'account': request.operator_name,
        'identity': request.operator_level,
        'ip': request.operator_obj.last_ip,
        'last_time': request.operator_obj.last_time,
        'login_count': request.operator_obj.login_count,
    }
    return render(request, 'index.html', {'data': data_list, 'info': account_info})


def account_unique(request):
    get_account = request.GET.get('account')

    if models.Admin.objects.filter(account=get_account):
        return JsonResponse({'state': 1})
    else:
        return JsonResponse({'state': 0})


def image_upload(request):
    file = request.FILES.get('file')
    judge = request.POST['filename'].split('+')[0]
    img_name = request.POST['filename'].split('+')[1]
    if judge == '1':  # 轮播图
        url = request.banner_images + img_name
    elif judge == '2':  # app菜单
        url = request.app_menu_images + img_name
    elif judge == '3':  # 推荐店铺
        url = request.recommend_shops_images + img_name
    elif judge == '4':  # 配送员头像
        url = request.distributor_image + img_name
    elif judge == '5':  # 上传商品图片
        url = request.goods_image + img_name
    UploadImg(url, file)
    return HttpResponse(1)


def kindeditor(request):
    print(request.POST.get('content'))
    return render(request, 'kind.html')


def upload_img(request):
    file_obj = request.FILES.get('imgFile')
    if file_obj.name.split('.')[-1] not in ['jpg', 'png', 'jpeg', 'gif', 'bmp', 'webp']:  # 判断上传不为图片
        return HttpResponse('<h2>只能上传图片哦</h2>')
    file_name = str(time.time()) + file_obj.name
    url = "/static/illustratio/"+file_name
    UploadImg(url, file_obj)
    resp = {
        "error":0,
        "url":"http://ftp.college.cqgynet.com"+url
    }
    return JsonResponse(resp)
