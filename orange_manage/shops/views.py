from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum, Q, F
from orange_manage import models
from orange_manage.utils import area_data as area
import json


def shop_list(request):
    '''
    商户列表
    '''
    get_pagesize = 15
    all_money = models.Shop.objects.values('money').aggregate(all_money=Sum('money'))['all_money']
    if request.method == 'GET':
        cookies_obj = request.COOKIES.get('data')
        get_page = request.GET.get('p', '1')
        if not cookies_obj:
            province_name = '0'
            city_name = '0'
            area_name = '0'
            searchtype = 'shop_name'
            filter_content = None
            get_status = '3'
            get_searchorder = 'shop_id'
        else:
            cookies_obj = eval(cookies_obj)
            province_name = cookies_obj['province_idss']  # 省名,
            city_name = cookies_obj['city_idss']  # 市名,'全部市'
            area_name = cookies_obj['area_id']  # 区名,'全部区'
            searchtype = cookies_obj['searchtype']  # (shop_name,phone_number,shop_id)查找内容分类
            filter_content = cookies_obj['keyword']  # 查找内容
            get_status = cookies_obj['searchstatus']  # 商店状态,'1'
            get_searchorder = cookies_obj['searchorder']  # 排序方式,'shop_id'
        get_status = ['0', '1', '2'] if get_status == '3' else list(get_status)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if province_name == '0':
            if filter_content:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(shop_name__contains=filter_content,
                                                          status__in=get_status).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(phone_number__contains=filter_content,
                                                          status__in=get_status).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(shop_id__contains=filter_content,
                                                          status__in=get_status).all().order_by(
                        get_searchorder)
                data_list = []
                if request.operator_region == 0:
                    data_obj = data_obj.filter(auth=2)
                else:
                    data_obj = data_obj.filter(auth=2, region_id=request.operator_region)
                for i in data_obj[start_nun:end_num]:
                    l_obj = models.ShopAssistant.objects.filter(shop_assistant_id=i.manager_id).first()
                    data_dict = {
                        'shop_id': i.shop_id,
                        'shop_name': i.shop_name,
                        'phone_number': i.phone_number,
                        'last_login': l_obj.last_login,
                        'money': i.money,
                        'status': i.status,
                    }
                    data_list.append(data_dict)
            else:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(status__in=get_status).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status).all().order_by(get_searchorder)
                data_list = []
                if request.operator_region == 0:
                    data_obj = data_obj.filter(auth=2)
                else:
                    data_obj = data_obj.filter(auth=2, region_id=request.operator_region)
                for i in data_obj[start_nun:end_num]:
                    l_obj = models.ShopAssistant.objects.filter(shop_assistant_id=i.manager_id).first()
                    data_dict = {
                        'shop_id': i.shop_id,
                        'shop_name': i.shop_name,
                        'phone_number': i.phone_number,
                        'last_login': l_obj.last_login,
                        'money': i.money,
                        'status': i.status,
                    }
                    data_list.append(data_dict)
        elif city_name == '0':
            region_obj = models.Region.objects.filter(province_id=province_name).all()
            region_list = []
            for i in region_obj:
                region_list.append(i.region_id)
            if filter_content:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(shop_name__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(phone_number__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(shop_id__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            else:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if request.operator_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=request.operator_region)
            for i in data_obj[start_nun:end_num]:
                l_obj = models.ShopAssistant.objects.filter(shop_assistant_id=i.manager_id).first()
                data_dict = {
                    'shop_id': i.shop_id,
                    'shop_name': i.shop_name,
                    'phone_number': i.phone_number,
                    'last_login': l_obj.last_login,
                    'money': i.money,
                    'status': i.status,
                }
                data_list.append(data_dict)
        elif area_name == '0':
            region_obj = models.Region.objects.filter(province_id=province_name, city_id=city_name).all()
            region_list = []
            for i in region_obj:
                region_list.append(i.region_id)
            if filter_content:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(shop_name__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(phone_number__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(shop_id__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            else:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if request.operator_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=request.operator_region)
            for i in data_obj[start_nun:end_num]:
                l_obj = models.ShopAssistant.objects.filter(shop_assistant_id=i.manager_id).first()
                data_dict = {
                    'shop_id': i.shop_id,
                    'shop_name': i.shop_name,
                    'phone_number': i.phone_number,
                    'last_login': l_obj.last_login,
                    'money': i.money,
                    'status': i.status,
                }
                data_list.append(data_dict)
        else:
            region_obj = models.Region.objects.filter(province_id=province_name, city_id=city_name,
                                                      area_id=area_name).all()
            region_list = []
            for i in region_obj:
                region_list.append(i.region_id)
            if filter_content:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(shop_name__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(phone_number__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(shop_id__contains=filter_content, status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            else:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,
                                                          region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if request.operator_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=request.operator_region)
            for i in data_obj[start_nun:end_num]:
                l_obj = models.ShopAssistant.objects.filter(shop_assistant_id=i.manager_id).first()
                data_dict = {
                    'shop_id': i.shop_id,
                    'shop_name': i.shop_name,
                    'phone_number': i.phone_number,
                    'last_login': l_obj.last_login,
                    'money': i.money,
                    'status': i.status,
                }
                data_list.append(data_dict)
        if len(data_obj) % int(get_pagesize):
            page_total = len(data_obj) // int(get_pagesize) + 1
        else:
            page_total = len(data_obj) // int(get_pagesize)
        if not filter_content: filter_content = ''
        status_all = {
            'province_name': province_name,
            'city_name': city_name,
            'area_name': area_name,
            'searchtype': searchtype,
            'filter_content': filter_content,
            'get_status': get_status,
            'get_status_len': len(get_status),
            'get_searchorder': get_searchorder,
        }
        return render(request, 'Merchant/index.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total), 'all_money': all_money,
                       'status_info': status_all})
    if request.method == 'POST':
        province_name = request.POST.get('province_idss')  # 省名
        city_name = request.POST.get('city_idss')  # 市名
        area_name = request.POST.get('area_id')  # 区名
        searchtype = request.POST.get('searchtype')  # (shop_name,phone_number,shop_id)查找内容分类
        filter_content = request.POST.get('keyword')  # 查找内容
        get_status = request.POST.get('searchstatus')  # 商店状态
        get_searchorder = request.POST.get('searchorder')  # 排序方式
        data_dict = {'province_idss': province_name,
                     'city_idss': city_name,
                     'area_id': area_name,
                     'searchtype': searchtype,
                     'keyword': filter_content,
                     'searchstatus': get_status,
                     'searchorder': get_searchorder,
                     }
        response = redirect('/admin/shop_list/')
        response.set_cookie('data', data_dict, 600)
        return response


def shop_edit(request):
    '''
   商户编辑
    '''
    if request.method == "GET":
        get_shop_id = int(request.GET.get('shop_id'))
        shop_obj = models.Shop.objects.filter(shop_id=get_shop_id).all()
        for i in shop_obj:
            region_obj = models.Region.objects.filter(region_id=i.region_id).first()
            province_obj = models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
            province_name = province_obj.site_name
            city_obj = models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
            city_name = city_obj.site_name
            area_obj = models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
            area_name = area_obj.site_name
            region_obj = models.Region.objects.filter(region_id=region_obj.region_id).first()
            shop_dict = {
                'shop_id': get_shop_id,
                'shop_name': i.shop_name,
                'packing_commission': i.packing_commission,
                'phone_number': i.phone_number,
                'region_id': i.region_id,
                'status': i.status,
            }
            region_dict = {
                'province_name': province_name,
                'city_name': city_name,
                'area_name': area_name,
                'region_name': region_obj.region_name,
            }
        return render(request, 'Merchant/form.html', {'shop_dict': shop_dict, 'region_dict': region_dict})
    if request.method == "POST":
        get_shop_id = request.POST.get('shop_id')
        get_name = request.POST.get('name')
        get_packing_commission = request.POST.get('Radios')
        get_phone_number = request.POST.get('phone')
        get_status = request.POST.get('options')
        get_region_id = request.POST.get('region_id')
        try:
            get_region_id = int(get_region_id)
        except ValueError:
            obj = models.Shop.objects.filter(shop_id=get_shop_id).first()
            get_region_id = obj.region_id
        models.Shop.objects.filter(shop_id=get_shop_id).update(
            shop_name=get_name,
            packing_commission=get_packing_commission,
            phone_number=get_phone_number,
            status=get_status,
            region_id=get_region_id,
        )
        return HttpResponse(1)


def store_form(request):
    '''
    审核商店
    '''
    try:
        if request.method == "GET":
            get_shop_id = request.GET.get('shop_id')
            shop_obj = models.Shop.objects.filter(shop_id=get_shop_id).first()
            assistant_obj = models.ShopAssistant.objects.filter(shop_assistant_id=shop_obj.manager_id).first()
            region_obj = models.Region.objects.filter(region_id=shop_obj.region_id).first()
            province_obj = models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
            city_obj = models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
            area_obj = models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
            province_name = province_obj.site_name
            city_name = city_obj.site_name
            area_name = area_obj.site_name
            try:
                x = json.loads(shop_obj.shop_photos)
                shop_obj.shop_photos = ''
                for i in x:
                    shop_obj.shop_photos += i + '，'
            except Exception:
                pass
            try:
                x = json.loads(shop_obj.business_license)
                shop_obj.business_license = ''
                for i in x:
                    shop_obj.business_license += i + '，'
            except Exception:
                pass
            shop_logo = shop_obj.shop_logo.split('，') if shop_obj.shop_logo else []  # 商店logo
            business_license = shop_obj.business_license.split('，') if shop_obj.business_license else []  # 营业执照
            shop_photos = shop_obj.shop_photos.split('，') if shop_obj.shop_photos else []  # 商店场景图地址列表
            catering_license = shop_obj.catering_license.split('，') if shop_obj.catering_license else []  # 食品安全地址列表
            data = {
                'shop_id': get_shop_id,
                'shop_name': shop_obj.shop_name,
                'shop_logo': shop_logo,
                # 'university_name':shop_obj.university_id,不存在了
                'campus_name': shop_obj.campus_id,
                'region_name': region_obj.region_name,
                'phone_number': shop_obj.phone_number,
                'manager_phone': assistant_obj.phone_number,
                'shop_type': shop_obj.shop_type,
                'in_area': province_name + city_name + area_name,
                'address': shop_obj.address,
                'business_license': business_license,
                'catering_license': catering_license,
                'bank_account': shop_obj.bank_account,
                'bank_account_holder': shop_obj.bank_account_holder,
                'shop_photos': shop_photos,  # 场景图
                'manage_name': assistant_obj.username,
            }
            return render(request, 'Merchant/store_form.html', {'data': data})
        if request.method == "POST":
            get_shop_id = request.POST.get('shop_id')
            get_auth = request.POST.get('auth')
            get_remark = request.POST.get('remark')
            models.Shop.objects.filter(shop_id=get_shop_id).update(auth=get_auth)
            models.ShopAuditLog.objects.create(shop_id=get_shop_id, auth=get_auth, operator_id=request.operator_id,
                                               remark=get_remark, create_time=timezone.now())
            return HttpResponse(1)
    except Exception:
        pass


def status_form(request):
    '''
    审核成功
    '''
    if request.method == "GET":
        get_shop_id = request.GET.get('shop_id')
        shop_obj = models.Shop.objects.filter(shop_id=get_shop_id).first()
        assistant_obj = models.ShopAssistant.objects.filter(shop_assistant_id=shop_obj.manager_id).first()
        region_obj = models.Region.objects.filter(region_id=shop_obj.region_id).first()
        province_obj = models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
        city_obj = models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
        area_obj = models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
        province_name = province_obj.site_name
        city_name = city_obj.site_name
        area_name = area_obj.site_name
        try:
            x = json.loads(shop_obj.shop_photos)
            shop_obj.shop_photos = ''
            for i in x:
                shop_obj.shop_photos += i + '，'
        except Exception:
            pass
        try:
            x = json.loads(shop_obj.business_license)
            shop_obj.business_license = ''
            for i in x:
                shop_obj.business_license += i + '，'
        except Exception:
            pass
        shop_logo = shop_obj.shop_logo.split('，') if shop_obj.shop_logo else []  # 商店logo
        business_license = shop_obj.business_license.split('，') if shop_obj.business_license else []  # 营业执照
        shop_photos = shop_obj.shop_photos.split('，') if shop_obj.shop_photos else []  # 商店场景图地址列表
        catering_license = shop_obj.catering_license.split('，') if shop_obj.catering_license else []  # 食品安全地址列表
        data = {
            'shop_id': get_shop_id,
            'shop_name': shop_obj.shop_name,
            'shop_logo': shop_logo,
            # 'university_name': shop_obj.university_id,
            'campus_name': shop_obj.campus_id,
            'region_name': region_obj.region_name,
            'phone_number': shop_obj.phone_number,
            'manager_phone': assistant_obj.phone_number,
            'shop_type': shop_obj.shop_type,
            'in_area': province_name + city_name + area_name,
            'address': shop_obj.address,
            'business_license': business_license,
            'catering_license': catering_license,
            'bank_account': shop_obj.bank_account,
            'bank_account_holder': shop_obj.bank_account_holder,
            'shop_photos': shop_photos,  # 场景图
            'manage_name': assistant_obj.username,
        }
        return render(request, 'Merchant/status_form.html', {'data': data})


def fail_form(request):
    '''
    审核失败
    '''
    if request.method == 'GET':
        get_shop_id = request.GET.get('shop_id')
        shop_obj = models.Shop.objects.filter(shop_id=get_shop_id).first()
        assistant_obj = models.ShopAssistant.objects.filter(shop_assistant_id=shop_obj.manager_id).first()
        region_obj = models.Region.objects.filter(region_id=shop_obj.region_id).first()
        province_obj = models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
        city_obj = models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
        area_obj = models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
        province_name = province_obj.site_name
        city_name = city_obj.site_name
        area_name = area_obj.site_name
        try:
            x = json.loads(shop_obj.shop_photos)
            shop_obj.shop_photos = ''
            for i in x:
                shop_obj.shop_photos += i + '，'
        except Exception:
            pass
        try:
            x = json.loads(shop_obj.business_license)
            shop_obj.business_license = ''
            for i in x:
                shop_obj.business_license += i + '，'
        except Exception:
            pass
        shop_logo = shop_obj.shop_logo.split('，') if shop_obj.shop_logo else []  # 商店logo
        business_license = shop_obj.business_license.split('，') if shop_obj.business_license else []  # 营业执照
        shop_photos = shop_obj.shop_photos.split('，') if shop_obj.shop_photos else []  # 商店场景图地址列表
        catering_license = shop_obj.catering_license.split('，') if shop_obj.catering_license else []  # 食品安全地址列表
        remark_obj = models.ShopAuditLog.objects.filter(shop_id=get_shop_id).first()
        data = {
            'shop_id': get_shop_id,
            'shop_name': shop_obj.shop_name,
            'shop_logo': shop_logo,
            # 'university_name': shop_obj.university_id,
            'campus_name': shop_obj.campus_id,
            'region_name': region_obj.region_name,
            'phone_number': shop_obj.phone_number,
            'manager_phone': assistant_obj.phone_number,
            'shop_type': shop_obj.shop_type,
            'in_area': province_name + city_name + area_name,
            'address': shop_obj.address,
            'business_license': business_license,
            'catering_license': catering_license,
            'bank_account': shop_obj.bank_account,
            'bank_account_holder': shop_obj.bank_account_holder,
            'shop_photos': shop_photos,  # 场景图
            'manage_name': assistant_obj.username,
            'remark': remark_obj.remark,
        }
        return render(request, 'Merchant/fail_form.html', {'data': data})


def shop_delete(request):
    '''
   商户列表删除
    '''
    get_shop_id = request.GET.get('shop_id')
    models.Shop.objects.filter(shop_id=get_shop_id).delete()
    return JsonResponse({})


def region_info(request):
    '''
    省市区关联
    '''
    data = area.region_data()
    return JsonResponse({
        "code": 0,
        "data": data,
        "error_msg": "返回数据成功",
        "msg": "",
    })


def wait_store(request):
    '''
    待审核
    '''
    if request.method == "GET":
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        filter_content = request.GET.get('filter_content')
        if filter_content:
            if filter_content == '开启':
                status = 1
            elif filter_content == '关闭':
                status = 0
            else:
                status = 2
            try:
                filter_content = int(filter_content)
            except Exception:
                filter_content = filter_content
            if isinstance(filter_content, str):
                all_obj = models.Shop.objects.filter(
                    Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj = models.Shop.objects.filter(
                    Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(
                        phone_number__contains=filter_content) | Q(status=status))
            if request.operator_region == 0:
                all_obj = all_obj.filter(auth=0)
            else:
                all_obj = all_obj.filter(auth=0, region_id=request.operator_region)
        else:
            if request.operator_region == 0:
                all_obj = models.Shop.objects.filter(auth=0).all()
            else:
                all_obj = models.Shop.objects.filter(auth=0, region_id=request.operator_region).all()
        if request.operator_region: all_obj = all_obj.filter(region_id=request.operator_region)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'shop_id': i.shop_id,
                'shop_name': i.shop_name,
                'phone_number': i.phone_number,
                'update_time': i.update_time,
                'status': i.status,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/wait_store.html',
                      {'data': data_list, 'page_total': str(page_total), 'get_page': get_page,
                       'filter_content': filter_content})


def wait_store2(request):
    '''
    审核通过
    '''
    if request.method == "GET":
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        filter_content = request.GET.get('filter_content')
        if filter_content:
            if filter_content == '开启':
                status = 1
            elif filter_content == '关闭':
                status = 0
            else:
                status = 2
            try:
                filter_content = int(filter_content)
            except Exception:
                filter_content = filter_content
            if isinstance(filter_content, str):
                all_obj = models.Shop.objects.filter(
                    Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj = models.Shop.objects.filter(
                    Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(
                        phone_number__contains=filter_content) | Q(status=status))
            if request.operator_region == 0:
                all_obj = all_obj.filter(auth=2)
            else:
                all_obj = all_obj.filter(auth=2, region_id=request.operator_region)
        else:
            if request.operator_region == 0:
                all_obj = models.Shop.objects.filter(auth=2).all()
            else:
                all_obj = models.Shop.objects.filter(auth=2, region_id=request.operator_region).all()
        if request.operator_region: all_obj = all_obj.filter(region_id=request.operator_region)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'shop_id': i.shop_id,
                'shop_name': i.shop_name,
                'phone_number': i.phone_number,
                'update_time': i.update_time,
                'status': i.status,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/wait_store_status.html',
                      {'data': data_list, 'page_total': str(page_total), 'get_page': get_page,
                       'filter_content': filter_content})


def wait_store3(request):
    '''
    审核失败
    '''
    if request.method == "GET":
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        filter_content = request.GET.get('filter_content')
        if filter_content:
            if filter_content == '开启':
                status = 1
            elif filter_content == '关闭':
                status = 0
            else:
                status = 2
            try:
                filter_content = int(filter_content)
            except Exception:
                filter_content = filter_content
            if isinstance(filter_content, str):
                all_obj = models.Shop.objects.filter(
                    Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj = models.Shop.objects.filter(
                    Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(
                        phone_number__contains=filter_content) | Q(status=status))
            if request.operator_region == 0:
                all_obj = all_obj.filter(auth=1)
            else:
                all_obj = all_obj.filter(auth=1, region_id=request.operator_region)
        else:
            if request.operator_region == 0:
                all_obj = models.Shop.objects.filter(auth=1).all()
            else:
                all_obj = models.Shop.objects.filter(auth=1, region_id=request.operator_region).all()
        if request.operator_region: all_obj = all_obj.filter(region_id=request.operator_region)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'shop_id': i.shop_id,
                'shop_name': i.shop_name,
                'phone_number': i.phone_number,
                'update_time': i.update_time,
                'status': i.status,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/wait_store_fail.html',
                      {'data': data_list, 'page_total': str(page_total), 'get_page': get_page,
                       'filter_content': filter_content})


def category_list(request):
    '''
    分类列表
    '''
    get_pagesize = 15
    get_page = request.GET.get('p', '1')
    all_obj = models.ShopSort.objects.filter(parent_id=0).all()
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
        get_pagesize)
    data_list = []
    for i in all_obj.order_by('-priority')[start_nun:end_num]:
        data_dict = {
            'priority': i.priority,
            'sort_id': i.sort_id,
            'sort_name': i.sort_name,
            'status': i.state,
        }
        data_list.append(data_dict)
    return render(request, 'Merchant/category_list.html',
                  {'data': data_list, 'page_total': str(page_total), 'get_page': get_page})


def add_originalform(request):
    '''
   添加分类
    '''
    if request.method == "GET":
        return render(request, 'Merchant/add_originalform.html')
    if request.method == "POST":
        get_priority = request.POST.get('priority')
        get_sort_name = request.POST.get('sort_name')
        get_state = request.POST.get('state')
        models.ShopSort.objects.create(priority=get_priority, sort_name=get_sort_name, state=get_state, parent_id=0)
        return HttpResponse(1)


def edit_originalform(request):
    '''
    编辑分类
    '''
    if request.method == 'GET':
        get_sort_id = request.GET.get('shop_id')
        obj = models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        data = {
            'sort_id': get_sort_id,
            'sort_name': obj.sort_name,
            'priority': obj.priority,
            'state': obj.state
        }
        return render(request, 'Merchant/edit_originalform.html', {'data': data})
    elif request.method == 'POST':
        get_sort_id = request.POST.get('sort_id')
        get_sort_name = request.POST.get('sort_name')
        get_priority = request.POST.get('priority')
        get_state = request.POST.get('state')
        models.ShopSort.objects.filter(sort_id=get_sort_id).update(sort_name=get_sort_name, priority=get_priority,
                                                                   state=get_state, parent_id=0)
        return HttpResponse(1)
    elif request.method == 'DELETE':
        get_sort_id = request.GET.get('sort_id')
        models.ShopSort.objects.filter(sort_id=get_sort_id).delete()
        models.ShopSort.objects.filter(parent_id=get_sort_id).delete()
        return HttpResponse(1)


def check_childlist(request):
    '''
   子分类列表
    '''
    get_pagesize = 15
    get_page = request.GET.get('p', '1')
    get_parent_name = request.GET.get('name')
    get_parent_id = request.GET.get('sort_id')
    all_obj = models.ShopSort.objects.filter(parent_id=get_parent_id).all()
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
        get_pagesize)
    data_list = []
    for i in all_obj.order_by('priority')[start_nun:end_num]:
        data_dict = {}
        data_dict['sort_id'] = i.sort_id
        data_dict['sort_name'] = i.sort_name
        data_dict['priority'] = i.priority
        data_dict['state'] = i.state
        data_list.append(data_dict)
    return render(request, 'Merchant/category_childlist.html',
                  {'data': data_list, 'f_id': get_parent_id, 'name': get_parent_name, 'page_total': str(page_total),
                   'get_page': get_page})


def add_childform(request):
    '''
    添加子分类
    '''
    if request.method == 'GET':
        parent_id = request.GET.get("shop_id")
        return render(request, 'Merchant/add_childform.html', {'parent_id': parent_id})
    elif request.method == 'POST':
        get_parent_id = request.POST.get('parent_id')
        get_sort_name = request.POST.get('sort_name')
        get_priority = request.POST.get('priority')
        get_state = request.POST.get('state')
        models.ShopSort.objects.create(parent_id=get_parent_id, sort_name=get_sort_name, state=get_state,
                                       priority=get_priority)
        return HttpResponse(1)


def edit_childform(request):
    '''
    编辑子分类
    '''
    if request.method == 'GET':
        get_sort_id = request.GET.get('shop_id')
        obj = models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        data = {
            'sort_id': get_sort_id,
            'sort_name': obj.sort_name,
            'priority': obj.priority,
            'state': obj.state
        }
        return render(request, 'Merchant/edit_childlform.html', {'data': data})
    elif request.method == 'POST':
        get_sort_id = request.POST.get('sort_id')
        parent_obj = models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        obj = models.ShopSort.objects.filter(sort_id=parent_obj.parent_id).first()
        get_sort_name = request.POST.get('sort_name')
        get_priority = request.POST.get('priority')
        get_state = request.POST.get('state')
        models.ShopSort.objects.filter(sort_id=get_sort_id).update(sort_name=get_sort_name, priority=get_priority,
                                                                   state=get_state, parent_id=parent_obj.parent_id)
        return HttpResponse(1)
    elif request.method == 'DELETE':
        get_sort_id = request.GET.get('sort_id')
        models.ShopSort.objects.filter(sort_id=get_sort_id).delete()
        return HttpResponse(1)


def circle_list(request):
    get_page = request.GET.get('p', '1')
    get_pagesize = 15
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    get_region = request.operator_region
    all_obj = models.Circle.objects.all() if get_region == 0 else models.Circle.objects.filter(region_id=get_region)
    page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
        get_pagesize)
    data_list = []
    all_obj.query.group_by = ['region_id']
    for i in all_obj.order_by('-priority')[start_nun:end_num]:
        if get_region:
            obj = models.Region.objects.get(region_id=get_region)
        else:
            obj = models.Region.objects.get(region_id=i.region_id)
        region_name = obj.region_name
        data_dict = {
            'circle_id': i.circle_id,
            'circle_name': i.circle_name,
            'priority': i.priority,
            'region_name': region_name,
            'region_id': i.region_id,
        }
        data_list.append(data_dict)
    return render(request, 'Merchant/circle_list.html',
                  {'data': data_list, 'get_page': get_page, 'page_total': str(page_total)})


def add_circle(request):
    if request.method == 'GET':
        return render(request, 'Merchant/add_circle.html')
    elif request.method == 'POST':
        circle_name = request.POST.get('circle_name')
        priority = request.POST.get('priority')
        if request.operator_region:
            models.Circle.objects.create(circle_name=circle_name, priority=priority, region_id=request.operator_region)
            return HttpResponse(1)
        else:
            return HttpResponse(0)


def edit_circle(request):
    if request.method == 'GET':
        get_id = request.GET.get('id')
        obj = models.Circle.objects.get(circle_id=get_id)
        data = {
            'circle_id': obj.circle_id,
            'circle_name': obj.circle_name,
            'priority': obj.priority,
        }
        return render(request, 'Merchant/edit_circle.html', {'data': data})
    elif request.method == 'POST':
        get_id = request.POST.get('circle_id')
        get_circle_name = request.POST.get('circle_name')
        get_priority = request.POST.get('priority')
        if get_circle_name:
            models.Circle.objects.filter(circle_id=get_id).update(circle_name=get_circle_name, priority=get_priority)
        else:
            models.Circle.objects.filter(circle_id=get_id).update(priority=get_priority)
        return HttpResponse(1)
    elif request.method == 'DELETE':
        get_id = request.GET.get('circle_id')
        models.Circle.objects.filter(circle_id=get_id).delete()
        return HttpResponse(1)


def store_list(request):
    if request.method == 'GET':
        operator_region = request.GET.get('region_id')
        circle_id = request.GET.get('circle_id')
        all_circle = models.CircleShop.objects.filter(circle_id=circle_id).all()
        circle_list = []
        for i in all_circle:
            circle_list.append(i.shop_id)
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        all_obj = models.Shop.objects.filter(auth=2, status=1, region_id=operator_region).all()  # 审核通过，状态开启
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'shop_id': i.shop_id,
                'shop_name': i.shop_name,
                'address': i.address,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/store_list.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'region_id': operator_region, 'circle_id': circle_id, 'circle_list': circle_list})
    elif request.method == 'POST':
        get_circle_id = request.POST.get('circle_id')
        get_shop_list = request.POST.getlist('checkbox')
        if request.operator_region == 0:
            return HttpResponse(0)
        models.CircleShop.objects.filter(circle_id=get_circle_id).delete()
        for i in get_shop_list:
            models.CircleShop.objects.create(circle_id=get_circle_id, shop_id=i)
        return HttpResponse(1)


def wait_goods(request):
    if request.method == 'GET':
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if request.operator_region:
            shop_list = models.Shop.objects.filter(region_id=request.operator_region).values_list('shop_id', flat=True)
        else:
            shop_list = models.Shop.objects.values_list('shop_id', flat=True)
        all_obj = models.Goods.objects.filter(auth=0, shop_id__in=shop_list)
        get_filter_content = request.GET.get('filter_content')
        if get_filter_content:
            filter_list = models.Shop.objects.filter(shop_name__contains=get_filter_content).values_list('shop_id',
                                                                                                         flat=True)
            all_obj = all_obj.filter(shop_id__in=filter_list)
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj.order_by('shop_id')[start_nun:end_num]:
            obj = models.Shop.objects.get(shop_id=i.shop_id)
            data_dict = {
                'goods_id': i.goods_id,
                'goods_name': i.goods_name,
                'shop_name': obj.shop_name,
                'unit_price': i.unit_price,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/wait_goods.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'filter_content': get_filter_content})
    elif request.method == 'POST':
        try:
            get_id = request.GET.get('goods_id')
            get_judge = request.GET.get('judge')  # 判断审核通过还是失败
            if get_judge:
                get_reason = request.GET.get('reason')
                data = {
                    'goods_id': get_id,
                    'reason': get_reason,
                    'create_time': timezone.now(),
                    'operator': request.operator_id,
                }
                models.GoodsExamineLog.objects.create(**data)
                models.Goods.objects.filter(goods_id=get_id).update(auth=2)  # 审核失败
            else:
                models.Goods.objects.filter(goods_id=get_id).update(auth=1)  # 审核通过
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)


def goods_details(request):
    get_id = request.GET.get('goods_id')
    obj = models.Goods.objects.get(goods_id=get_id)
    shop_obj = models.Shop.objects.get(shop_id=obj.shop_id)
    classify_obj = models.GoodsClassify.objects.get(record_id=obj.classify_id)
    classify_name = classify_obj.name
    platform_classify_obj = models.GoodsClassifyPlatform.objects.get(record_id=obj.platform_classify_id)
    platform_classify_name = platform_classify_obj.name
    if classify_obj.parent_id != -1:
        c_obj = models.GoodsClassify.objects.get(record_id=classify_obj.parent_id)
        classify_name = c_obj.name + ' ' + classify_name
    if platform_classify_obj.parent_id != -1:
        p_obj = models.GoodsClassifyPlatform.objects.get(record_id=platform_classify_obj.parent_id)
        platform_classify_name = p_obj.name + ' ' + platform_classify_name
    data = {
        'shop_name': shop_obj.shop_name,
        'goods_name': obj.goods_name,
        'image': request.FTP_HOST + request.goods_image + obj.image,
        'product_code': obj.product_code,  # 条码
        'is_recycle': obj.is_recycle,  # 是否使用需回收包装
        'classify_name': classify_name,  # 商家分类名字
        'platform_classify_name': platform_classify_name,  # 平台分类名字
        'original_price': obj.original_price,  # 进价
        'unit_price': obj.unit_price,  # 售价
        'judge': 0,  # 为单规格
    }
    add_obj = models.GoodsSpecification.objects.filter(goods_id=get_id)
    if add_obj:  # 多规格
        data['judge'] = 1
        data_list = []
        for i in add_obj:
            data_dict = {
                'unit_price': i.unit_price,  # 售价
                'original_price': i.original_price,  # 进价
            }
            name = ''
            spec = eval(i.spec)
            for j in spec:
                spec_obj = models.GoodsSpecValue.objects.get(spec_value_id=j)
                name += spec_obj.spec_value + ' '
            data_dict['name'] = name
            data_list.append(data_dict)
        data['add'] = data_list
    return render(request, 'Merchant/goods_details.html', {'data': data})


def nopass_goods(request):
    if request.method == 'GET':
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if request.operator_region:
            shop_list = models.Shop.objects.filter(region_id=request.operator_region).values_list('shop_id', flat=True)
        else:
            shop_list = models.Shop.objects.values_list('shop_id', flat=True)
        all_obj = models.Goods.objects.filter(auth=2, shop_id__in=shop_list)
        get_filter_content = request.GET.get('filter_content')
        if get_filter_content:
            filter_list = models.Shop.objects.filter(shop_name__contains=get_filter_content).values_list('shop_id',
                                                                                                         flat=True)
            all_obj = all_obj.filter(shop_id__in=filter_list)
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj.order_by('shop_id')[start_nun:end_num]:
            obj = models.Shop.objects.get(shop_id=i.shop_id)
            reason_obj = models.GoodsExamineLog.objects.get(goods_id=i.goods_id)
            data_dict = {
                'goods_id': i.goods_id,
                'goods_name': i.goods_name,
                'shop_name': obj.shop_name,
                'unit_price': i.unit_price,
                'reason': reason_obj.reason,
            }
            data_list.append(data_dict)
        return render(request, 'Merchant/wait_goods_fail.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'filter_content': get_filter_content})
