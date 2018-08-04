from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from orange_manage import models
import json, hashlib


def account_list(request):
    '''
    管理员列表
    '''
    get_pagesize = 15
    get_page = request.GET.get('p', '1')
    get_account = request.session['user']
    obj = models.Admin.objects.filter(account=get_account).first()
    get_level = obj.level
    if get_level == 0:
        all_obj = models.Admin.objects.filter(level__lt=2).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj.order_by('level')[start_nun:end_num]:
            region_obj = models.Region.objects.filter(region_id=i.open_admin_region).first()
            if not region_obj:
                region_name = '平台所有区域'
            else:
                region_name = region_obj.region_name
            data_dict = {
                'id': i.id,
                'account': i.account,
                'realname': i.realname,
                'phone': i.phone,
                'email': i.email,
                'qq': i.qq,
                'last_ip': i.last_ip,
                'last_time': i.last_time,
                'login_count': i.login_count,
                'status': i.status,
                'level': i.level,
                'nickname': i.nickname,
                'open_admin_region': region_name,
            }
            data_list.append(data_dict)
    if get_level == 1:
        all_obj = models.Admin.objects.filter(level=2, open_admin_region=obj.open_admin_region).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            region_obj = models.Region.objects.filter(region_id=i.open_admin_region).first()
            data_dict = {
                'id': i.id,
                'account': i.account,
                'realname': i.realname,
                'phone': i.phone,
                'email': i.email,
                'qq': i.qq,
                'last_ip': i.last_ip,
                'last_time': i.last_time,
                'login_count': i.login_count,
                'status': i.status,
                'level': i.level,
                'nickname': i.nickname,
                'open_admin_region': region_obj.region_name,
            }
            data_list.append(data_dict)
    return render(request, 'Index/account.html',
                  {'data': data_list, 'get_page': get_page, 'page_total': str(page_total)})


def add_account(request):
    '''
    添加管理员
    '''
    if request.method == 'GET':
        operate_name = request.session.get('user')
        obj = models.Admin.objects.filter(account=operate_name).first()
        operate_level = obj.level
        operate_region = obj.open_admin_region
        return render(request, 'Index/add_accountform.html', {'level': operate_level, 'region_id': operate_region})
    elif request.method == 'POST':
        print(request.POST)
        get_operator = request.session.get('user')
        operator_obj = models.Admin.objects.filter(account=get_operator).first()
        get_account = request.POST.get('account')
        get_pwd = request.POST.get('pwd')
        hash_key = hashlib.sha256()
        hash_key.update(get_pwd.encode())
        get_pwd = hash_key.hexdigest()
        get_realname = request.POST.get('realname')
        get_phone = request.POST.get('phone')
        get_email = request.POST.get('email')
        get_qq = request.POST.get('qq')
        get_level = request.POST.get('level')
        get_region = request.POST.get('region_id')
        if get_region:
            get_region = get_region
        else:
            if get_level == '2':
                operate_name = request.session.get('user')
                obj = models.Admin.objects.filter(account=operate_name).first()
                get_region = obj.open_admin_region
            else:
                get_region = 0
        get_menus = request.POST.get('authoritydata')
        get_menus = get_menus.split(',')
        all_obj = models.Menu.objects.filter(field_function_name__in=get_menus).exclude(parent_id=0)
        parent_list = []
        for i in all_obj:
            if i.parent_id not in parent_list:
                parent_list.append(i.parent_id)
        data_list = []
        for i in parent_list:
            parent_dict = {}
            son_list = []
            for j in all_obj.filter(parent_id=i).all():
                son_list.append(j.id)
            parent_dict[i] = son_list
            data_list.append(parent_dict)
        if not data_list: data_list = json.loads(operator_obj.menus)
        data_list = json.dumps(data_list)
        models.Admin.objects.create(account=get_account, pwd=get_pwd, realname=get_realname, phone=get_phone,
                                    email=get_email, qq=get_qq, login_count=0, status=1, level=get_level,
                                    open_admin_region=get_region, menus=data_list, last_time=timezone.now())
        return HttpResponse(1)


def permissions(request):
    '''
    显示能够赋予权限
    '''
    if request.method == 'GET':
        operate_name = request.session.get('user')
        obj = models.Admin.objects.filter(account=operate_name).first()
        menus_list = json.loads(obj.menus)
        data_list = []
        for i in menus_list:
            for key, value in i.items():
                index_obj = models.Menu.objects.filter(id=key).first()
                index_name = index_obj.field_function_name
                data_dict = {}
                child_list = []
                for j in value:
                    child_obj = models.Menu.objects.filter(id=j).first()
                    child_name = child_obj.field_function_name
                    child_list.append(child_name)
                data_dict[index_name] = child_list
            data_list.append(data_dict)
        return JsonResponse(data_list, safe=False)


def edit_accountinfo(request):
    if request.method == 'GET':
        get_parent = request.session.get('user')
        parent_obj = models.Admin.objects.filter(account=get_parent).first()
        get_admin_id = request.GET.get('shop_id')
        obj = models.Admin.objects.filter(id=get_admin_id).first()
        if obj.open_admin_region:
            obj_region = models.Region.objects.filter(region_id=obj.open_admin_region).first()
            province_obj = models.AddresLibrary.objects.filter(id=obj_region.province_id).first()
            city_obj = models.AddresLibrary.objects.filter(id=obj_region.city_id).first()
            area_obj = models.AddresLibrary.objects.filter(id=obj_region.area_id).first()
            data = {
                'account': obj.account,
                'realname': obj.realname,
                'phone': obj.phone,
                'email': obj.email,
                'qq': obj.qq,
                'last_ip': obj.last_ip,
                'last_time': obj.last_time,
                'login_count': obj.login_count,
                'status': obj.status,
                'level': obj.level,
                'nickname': obj.nickname,
                'province_name': province_obj.site_name,
                'city_name': city_obj.site_name,
                'area_name': area_obj.site_name,
                'region_name': obj_region.region_name,
            }
        else:
            data = {
                'account': obj.account,
                'realname': obj.realname,
                'phone': obj.phone,
                'email': obj.email,
                'qq': obj.qq,
                'last_ip': obj.last_ip,
                'last_time': obj.last_time,
                'login_count': obj.login_count,
                'status': obj.status,
                'level': obj.level,
                'nickname': obj.nickname,
                'province_name': '',
                'city_name': '',
                'area_name': '',
                'region_name': '',
            }

        return render(request, 'Index/edit_accountinfo.html', {'data': data, 'parent_level': parent_obj.level})
    elif request.method == 'POST':
        get_account = request.POST.get('account')
        get_pwd = request.POST.get('pwd')
        get_realname = request.POST.get('realname')
        get_phone = request.POST.get('phone')
        get_email = request.POST.get('email')
        get_qq = request.POST.get('qq')
        get_status = request.POST.get('status')
        get_level = request.POST.get('level')
        get_region = request.POST.get('region_id')
        if get_level == 0:
            get_region = 0
        elif get_level == 1:
            get_region = get_region
        else:
            operate_name = request.session.get('user')
            obj = models.Admin.objects.filter(account=operate_name).first()
            get_region = obj.open_admin_region
        if get_pwd:
            models.Admin.objects.filter(account=get_account).update(pwd=get_pwd, realname=get_realname, phone=get_phone,
                                                                    email=get_email, qq=get_qq, status=get_status,
                                                                    level=get_level, open_admin_region=get_region)
        else:
            models.Admin.objects.filter(account=get_account).update(realname=get_realname, phone=get_phone,
                                                                    email=get_email, qq=get_qq, status=get_status,
                                                                    level=get_level, open_admin_region=get_region)
        return redirect('/admin/account_list/')
    elif request.method == 'DELETE':
        get_id = request.GET.get('account_id')
        models.Admin.objects.filter(id=get_id).delete()
        return HttpResponse(0)


def edit_authorityform(request):
    if request.method == 'GET':
        get_id = request.GET.get('shop_id')
        obj = models.Admin.objects.filter(id=get_id).first()
        obj_list = []
        for i in json.loads(obj.menus):
            for key, val in i.items():
                obj_list.append(key)
                for j in val:
                    obj_list.append(j)
        data_list = []
        for i in obj_list:
            permission_name = models.Menu.objects.filter(id=i).values_list('field_function_name')[0][0]
            data_list.append(permission_name)
        return render(request, 'Index/edit_authorityform.html', {'data': data_list, 'id': get_id})
    elif request.method == 'POST':
        print(request.POST)
        get_permissions = json.loads(request.POST.get('gmx'))
        get_id = request.POST.get('id')
        print(get_permissions)
        all_obj = models.Menu.objects.filter(field_function_name__in=get_permissions).exclude(parent_id=0)
        parent_list = []
        for i in all_obj:
            if i.parent_id not in parent_list:
                parent_list.append(i.parent_id)
        data_list = []
        for i in parent_list:
            parent_dict = {}
            son_list = []
            for j in all_obj.filter(parent_id=i).all():
                son_list.append(j.id)
            parent_dict[i] = son_list
            data_list.append(parent_dict)
        data_list = json.dumps(data_list)
        models.Admin.objects.filter(id=get_id).update(menus=data_list)
        return HttpResponse(1)
