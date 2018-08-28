from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from orange_manage import models
from orange_manage.utils.password_encryption import pwd_encrypted
import json


def account_list(request):
    """管理员列表"""
    get_pagesize = 15
    get_page = request.GET.get('p', '1')
    get_level = request.operator_level
    if get_level == 0:
        all_obj = models.Admin.objects.filter(level__lt=2)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        status = {
            'keyword': request.GET.get('keyword'),
            'searchtype': request.GET.get('searchtype'),
        }
        if request.GET.get('keyword'):
            if request.GET.get('searchtype') == 'realname':
                all_obj = all_obj.filter(realname__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'account':
                all_obj = all_obj.filter(account__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'phone':
                all_obj = all_obj.filter(phone__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'admin_id':
                all_obj = all_obj.filter(id=request.GET.get('keyword'))
        all_obj = all_obj.exclude(id=request.operator_id)
        for i in all_obj.order_by('level')[start_nun:end_num]:
            region_obj = models.Region.objects.filter(region_id=i.open_admin_region).first()
            region_name = region_obj.region_name if region_obj else '平台所有区域'
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
        all_obj = models.Admin.objects.filter(level=2, open_admin_region=request.operator_region).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        status = {
            'keyword': request.GET.get('keyword'),
            'searchtype': request.GET.get('searchtype'),
        }
        if request.GET.get('keyword'):
            if request.GET.get('searchtype') == 'realname':
                all_obj = all_obj.filter(realname__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'account':
                all_obj = all_obj.filter(account__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'phone':
                all_obj = all_obj.filter(phone__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'admin_id':
                all_obj = all_obj.filter(id=request.GET.get('keyword'))
        all_obj = all_obj.exclude(id=request.operator_id)
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
                  {'data': data_list, 'get_page': get_page, 'page_total': str(page_total), 'status': status})


def add_account(request):
    """添加管理员"""
    if request.method == 'GET':
        operate_level = request.operator_level
        operate_region = request.operator_region
        return render(request, 'Index/add_accountform.html', {'level': operate_level, 'region_id': operate_region})
    elif request.method == 'POST':
        get_account = request.POST.get('account')
        get_pwd = pwd_encrypted(request.POST.get('pwd'))
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
                get_region = request.operator_region
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
        if not data_list: data_list = json.loads(request.operator_menus)
        data_list = json.dumps(data_list)
        models.Admin.objects.create(account=get_account, pwd=get_pwd, realname=get_realname, phone=get_phone,
                                    email=get_email, qq=get_qq, login_count=0, status=1, level=get_level,
                                    open_admin_region=get_region, menus=data_list, last_time=timezone.now())
        return HttpResponse(1)


def set_authority(request):
    return render(request, 'Index/set_authority.html')


def permissions(request):
    '''
    显示能够赋予权限
    '''
    if request.method == 'GET':
        menus_list = json.loads(request.operator_menus)
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
        get_admin_id = request.GET.get('account_id')
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

        return render(request, 'Index/edit_accountinfo.html', {'data': data, 'parent_level': request.operator_level})
    elif request.method == 'POST':
        get_account = request.POST.get('account')
        get_pwd = pwd_encrypted(request.POST.get('pwd'))
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
            get_region = request.operator_region
        if get_pwd:
            models.Admin.objects.filter(account=get_account).update(pwd=get_pwd, realname=get_realname, phone=get_phone,
                                                                    email=get_email, qq=get_qq, status=get_status,
                                                                    level=get_level, open_admin_region=get_region)
        else:
            models.Admin.objects.filter(account=get_account).update(realname=get_realname, phone=get_phone,
                                                                    email=get_email, qq=get_qq, status=get_status,
                                                                    level=get_level, open_admin_region=get_region)
        return HttpResponse(1)
    elif request.method == 'DELETE':
        get_id = request.GET.get('account_id')
        models.Admin.objects.filter(id=get_id).delete()
        return HttpResponse(0)


def edit_authorityform(request):
    if request.method == 'GET':
        get_id = request.GET.get('account_id')
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
        get_permissions = json.loads(request.POST.get('gmx'))
        get_id = request.POST.get('id')
        all_obj = models.Menu.objects.filter(field_function_name__in=get_permissions).exclude(parent_id=0)
        parent_list = []
        for i in all_obj:
            if i.parent_id not in parent_list: parent_list.append(i.parent_id)
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


def edit_personinfo(request):
    if request.method == 'GET':
        data = {
            'account': request.operator_obj.account,
            'realname': request.operator_obj.realname,
            'phone': request.operator_obj.phone,
            'email': request.operator_obj.email,
            'qq': request.operator_obj.qq,
        }
        return render(request, 'Index/personinfo.html', {'data': data})
    elif request.method == 'POST':
        get_new_pass = request.POST.get('new_pass')
        get_pwd = pwd_encrypted(get_new_pass)
        get_realname = request.POST.get('realname')
        get_email = request.POST.get('email')
        get_phone = request.POST.get('phone')
        get_qq = request.POST.get('qq')
        obj = models.Admin.objects.filter(id=request.operator_id)
        if get_pwd:
            obj.update(pwd=get_pwd, realname=get_realname, email=get_email,
                       phone=get_phone, qq=get_qq)
        else:
            obj.update(realname=get_realname, email=get_email,
                       phone=get_phone, qq=get_qq)
        return HttpResponse(1)


def clear_key(request):
    get_id = request.GET.get('id')
    models.Admin.objects.filter(id=get_id).update(admin_key=None)
    return HttpResponse(1)


def choose_address(request):
    try:
        if request.GET.get('flag') == 'a':  # 为区县
            all_obj = models.AddresLibrary.objects.filter(superior_id=request.GET.get('id'))
            msg = '区县名称'
        elif request.GET.get('flag') == 'c':  # 为市:
            all_obj = models.AddresLibrary.objects.filter(superior_id=request.GET.get('id'))
            msg = '市名称'
        # elif request.GET.get('flag') == 'a':  # 为区县:
        else:  # 为省:
            all_obj = models.AddresLibrary.objects.filter(character=0)
            msg = '省名称'
        if request.GET.get('keyword'): all_obj = all_obj.filter(site_name__contains=request.GET.get('keyword'))
        data_list = []
        for i in all_obj:
            data = []
            data.append(i.id)
            data.append(i.site_name)
            data_list.append(data)
        return render(request, 'Index/AddresLibraryList.html',
                      {'data': data_list, 'msg': msg, 'flag': request.GET.get('flag'), 'id': request.GET.get('id')})
    except Exception:
        return HttpResponse('<h2>请选择具体的省市区</h2>')


def region_list(request):
    get_id = request.GET.get('id')
    all_obj = models.Region.objects.filter(area_id=get_id)
    data_list = []
    if all_obj:
        for i in all_obj:
            data_dict = {
                'region_id': i.region_id,
                'region_name': i.region_name,
            }
            data_list.append(data_dict)
    return render(request, 'Index/RegionList.html', {'data': data_list, 'area_id': get_id})


def add_region(request):
    if request.method == 'POST':
        get_name = request.POST.get('region_name')
        get_area_id = request.POST.get('area_id')
        city_obj = models.AddresLibrary.objects.get(id=get_area_id)
        city_id = city_obj.superior_id
        city_obj = models.AddresLibrary.objects.get(id=city_id)
        province_id = city_obj.superior_id
        models.Region.objects.create(region_name=get_name, province_id=province_id, city_id=city_id,
                                     area_id=get_area_id)
        return HttpResponse(1)
    return render(request, 'Index/add_region.html')


def exist_region(request):
    if request.method == 'GET':
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        all_obj = models.Region.objects.filter(
            region_id=request.operator_region) if request.operator_region else models.Region.objects.all()
        if request.GET.get('keyword'):
            obj = models.AddresLibrary.objects.filter(character=2, site_name__contains=request.GET.get('keyword'))
            obj_list = []
            for i in obj:
                obj_list.append(i.id)
            all_obj = all_obj.filter(area_id__in=obj_list)
        data_list = []
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        for i in all_obj[start_nun:end_num]:
            p_obj = models.AddresLibrary.objects.get(id=i.province_id)
            c_obj = models.AddresLibrary.objects.get(id=i.city_id)
            a_obj = models.AddresLibrary.objects.get(id=i.area_id)
            data_dict = {
                'region_id': i.region_id,
                'region_name': i.region_name,
                'province_name': p_obj.site_name,
                'city_name': c_obj.site_name,
                'area_name': a_obj.site_name,
            }
            data_list.append(data_dict)
        return render(request, 'Index/ExistingAreaList.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'operator_region': request.operator_region})
    elif request.method == 'DELETE':
        models.Region.objects.filter(region_id=request.GET.get('region_id')).delete()
        return HttpResponse(1)


def edit_region(request):
    if request.method == 'POST':
        get_name = request.POST.get('region_name')
        if not get_name: return HttpResponse(2)
        models.Region.objects.filter(region_id=request.POST.get('region_id')).update(region_name=get_name)
        return HttpResponse(1)
    return render(request, 'Index/edit_region.html')


def campus_list(request):
    if request.method == 'GET':
        get_id = request.GET.get('region_id')
        all_obj = models.RegionCampus.objects.filter(region_id=get_id)
        data_list = []
        for i in all_obj:
            obj = models.Campus.objects.get(campus_id=i.campus_id)
            if obj:
                data_dict = {
                    'campus_id': obj.campus_id,
                    'campus_name': obj.campus,
                }
                data_list.append(data_dict)
        return render(request, 'Index/CampusList.html', {'data': data_list, 'region_id': get_id})
    elif request.method == 'DELETE':
        get_id = request.GET.get('campus_id')
        models.Campus.objects.filter(campus_id=get_id).delete()
        models.RegionCampus.objects.filter(campus_id=get_id).delete()
        return HttpResponse(1)


def add_campusinfo(request):
    if request.method == 'POST':
        get_campus_name = request.POST.get('campus_name')
        get_region_id = request.POST.get('region_id')
        obj = models.Campus.objects.create(campus=get_campus_name)
        models.RegionCampus.objects.create(campus_id=obj.campus_id, region_id=get_region_id)
        return HttpResponse(1)
    return render(request, 'Index/add_campus.html')


def edit_campusinfo(request):
    if request.method == 'POST':
        try:
            get_campus_id = request.POST.get('campus_id')
            get_campus_name = request.POST.get('campus_name')
            models.Campus.objects.filter(campus_id=get_campus_id).update(campus=get_campus_name)
            return HttpResponse(1)
        except Exception:
            return HttpResponse(0)
    return render(request, 'Index/edit_campus.html')


def address_list(request):
    get_address_id = request.GET.get('address_id')
    all_obj = models.Address.objects.filter(campus_id=request.GET.get('campus_id'))
    all_obj = all_obj.filter(parent_id=get_address_id) if get_address_id else all_obj.filter(parent_id=-1)
    data_list = []
    for i in all_obj:
        data_dict = {
            'address_id': i.address_id,
            'campus_id': i.campus_id,
            'value': i.value,
            'cost': i.cost,
            'have_subordinate': i.have_subordinate,
            'gender': i.gender,
        }
        data_list.append(data_dict)
    return render(request, 'Index/AddressList.html', {'data': data_list, 'address_id': get_address_id , 'campus_id': request.GET.get('campus_id')})


def add_address(request):
    if request.method == 'POST':
        get_campus_id = request.POST.get('campus_id')
        get_parent_id = request.POST.get('address_id')
        get_info = request.POST.get('info')
        info_list = get_info.split('；')
        try:
            for i in info_list:
                if i == '': break
                value = i.split('，')[0]
                gender = i.split('，')[1]
                if gender == '男':
                    gender = 1
                elif gender == '女':
                    gender = 2
                else:
                    gender = 0
                cost = i.split('，')[2]
                if get_parent_id == 'None':
                    data = {
                        'campus_id': get_campus_id,
                        'parent_id': -1,
                        'value': value,
                        'cost': cost,
                        'gender': gender,
                        'have_subordinate': 0,
                    }
                else:
                    models.Address.objects.filter(address_id=get_parent_id).update(have_subordinate=1)
                    data = {
                        'campus_id': get_campus_id,
                        'parent_id': get_parent_id,
                        'value': value,
                        'cost': cost,
                        'gender': gender,
                        'have_subordinate': 0,
                    }
                models.Address.objects.create(**data)
            return HttpResponse(1)
        except Exception:
            return HttpResponse(0)
    return render(request, 'Index/add_address.html')


def edit_address(request):
    if request.method == 'POST':
        try:
            get_gender = request.POST.get('gender')
            if get_gender == '男':
                gender = 1
            elif get_gender == '女':
                gender = 2
            else:
                gender = 0
            data = {
                'value': request.POST.get('address_name'),
                'cost': request.POST.get('cost'),
                'gender': gender,
            }
            models.Address.objects.filter(address_id=request.POST.get('address_id')).update(**data)
            return HttpResponse(1)
        except Exception:
            return HttpResponse(0)
    elif request.method == 'DELETE':
        try:
            models.Address.objects.filter(address_id=request.GET.get('address_id')).delete()
            return HttpResponse(1)
        except Exception:
            return HttpResponse(0)
    return render(request, 'Index/edit_address.html')
