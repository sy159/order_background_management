from django.http import JsonResponse,QueryDict
from django.utils import timezone
from django.shortcuts import render, redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.db.models import Sum,Q,F
from orange_manage import models
from .tool import area_data as area
from .tool import login_validation as val
from .tool import produce_key as key
import json,time


# Create your views here.

@csrf_protect
def login(request):
    '''
    登陆跳转
    '''
    if request.method=='POST':
        get_ip = request.META['REMOTE_ADDR']
        last_time=timezone.now()
        get_name = request.POST.get('account', None)
        get_pwd = request.POST.get('pwd', None)
        get_verifycode = request.POST.get('verifycode')
        get_name_obj = models.Admin.objects.filter(account=get_name).first()
        if get_name_obj:  # 判断用户是否存在
            if get_name_obj.pwd == get_pwd:  # 判断密码是否正确
                judge = models.Admin.objects.filter(account=get_name).values_list('admin_key').first()[0]
                if judge:  # 判断是否第一次登陆
                    if val.validation(judge, get_verifycode):  # 判断验证码是否正确
                        request.session['user']=get_name
                        request.session['judge']=True
                        models.Admin.objects.filter(account=get_name).update(last_time=last_time,last_ip=get_ip,login_count=F('login_count')+1)
                        return redirect('/admin/index/')
                    else:
                        return render(request,'login.html',{'error_msg':'验证码错误'})
                else:
                    request.session['user'] = get_name
                    request.session['judge'] = True
                    models.Admin.objects.filter(account=get_name).update(last_time=last_time, last_ip=get_ip,login_count=F('login_count') + 1)
                    return redirect('/admin/bind_account/')
            return render(request,'login.html',{'error_msg':'密码错误'})
        return render(request,'login.html',{'error_msg':'该用户不存在'})
    else:
        return render(request,'login.html',{'error_msg':''})


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
    if request.method=="GET":
        if request.GET.get('erro'):
            erro='输入的校验错误，请重新绑定'
        else:
            erro=''
        account=request.session.get('user')
        keys=key.login_key()
        qr_code='otpauth://totp/'+account+'?secret='+keys
        return render(request,'bind_account.html',{'account':account,'key':keys,"code":qr_code,'erro':erro})
    elif request.method=="POST":
        get_account=request.session.get('user')
        get_key=request.POST.get('key')
        get_code=request.POST.get('check_code')
        if val.validation(get_key,get_code):
            models.Admin.objects.filter(account=get_account).update(admin_key=get_key)
            return redirect('/admin/index/')
        else:
            return redirect('/admin/bind_account/?erro=1')


def index(request):
    get_account=request.session.get('user')
    obj=models.Admin.objects.filter(account=get_account).first()
    menus_list=json.loads(obj.menus)
    data_list=[]
    for i in menus_list:
        for key,value in i.items():
            index_obj=models.Menu.objects.filter(id=key).first()
            index_name=index_obj.field_function_name
            data_dict={}
            child_list=[]
            for j in value:
                child_dict={}
                child_obj=models.Menu.objects.filter(id=j).first()
                child_name=child_obj.field_function_name
                child_url=child_obj.field_function_url
                child_dict['child_url']=child_url
                child_dict['child_name']=child_name
                child_list.append(child_dict)
            data_dict[index_name]=child_list
        data_list.append(data_dict)
    return render(request,'index.html',{'data':data_list,'account':get_account,'identity':obj.level})


def shop_list(request):
    '''
    商户列表
    '''
    get_pagesize = 15
    all_money_obj = models.Shop.objects.values('money').annotate(all_money=Sum('money'))
    all_money = all_money_obj[0]['all_money']
    get_operator=request.session.get('user')
    obj=models.Admin.objects.filter(account=get_operator).first()
    if request.method=='GET':
        cookies_obj=request.COOKIES.get('data')
        get_page = request.GET.get('p','1')
        if not cookies_obj:
            province_name='0'
            city_name='0'
            area_name='0'
            searchtype='shop_name'
            filter_content=None
            get_status='3'
            get_searchorder='shop_id'
        else:
            cookies_obj=eval(cookies_obj)
            province_name = cookies_obj['province_idss']  # 省名,
            city_name = cookies_obj['city_idss']  # 市名,'全部市'
            area_name = cookies_obj['area_id']  # 区名,'全部区'
            searchtype = cookies_obj['searchtype'] # (shop_name,phone_number,shop_id)查找内容分类
            filter_content = cookies_obj['keyword']  # 查找内容
            get_status = cookies_obj['searchstatus']  # 商店状态,'1'
            get_searchorder = cookies_obj['searchorder']  # 排序方式,'shop_id'
        if get_status=='3':
            get_status=['0','1','2']
        else:
            get_status=list(get_status)
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if province_name == '0':
            if filter_content:
                if searchtype == 'shop_name':
                    data_obj = models.Shop.objects.filter(shop_name__contains=filter_content,status__in=get_status).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(phone_number__contains=filter_content,
                                                          status__in =get_status).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(shop_id__contains=filter_content,
                                                          status__in=get_status).all().order_by(
                        get_searchorder)
                data_list = []
                if obj.open_admin_region==0:
                    data_obj = data_obj.filter(auth=2)
                else:
                    data_obj = data_obj.filter(auth=2, region_id=obj.open_admin_region)
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
                if obj.open_admin_region == 0:
                    data_obj = data_obj.filter(auth=2)
                else:
                    data_obj = data_obj.filter(auth=2, region_id=obj.open_admin_region)
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
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if obj.open_admin_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=obj.open_admin_region)
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
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if obj.open_admin_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=obj.open_admin_region)
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
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                elif searchtype == 'phone_number':
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
                else:
                    data_obj = models.Shop.objects.filter(status__in=get_status,region_id__in=region_list).all().order_by(get_searchorder)
            data_list = []
            if obj.open_admin_region == 0:
                data_obj = data_obj.filter(auth=2)
            else:
                data_obj = data_obj.filter(auth=2, region_id=obj.open_admin_region)
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
        status_all={
            'province_name':province_name,
            'city_name':city_name,
            'area_name':area_name,
            'searchtype':searchtype,
            'filter_content':filter_content,
            'get_status':get_status,
            'get_searchorder':get_searchorder,
        }
        return render(request, 'Merchant/index.html',{'data': data_list,'get_page':get_page, 'page_total': str(page_total),'all_money': all_money,'status_info':status_all})
    if request.method=='POST':
        province_name = request.POST.get('province_idss')  # 省名
        city_name = request.POST.get('city_idss')  # 市名
        area_name = request.POST.get('area_id')  # 区名
        searchtype = request.POST.get('searchtype')  # (shop_name,phone_number,shop_id)查找内容分类
        filter_content = request.POST.get('keyword')  # 查找内容
        get_status = request.POST.get('searchstatus')  # 商店状态
        get_searchorder = request.POST.get('searchorder')  # 排序方式
        data_dict={'province_idss':province_name,
                   'city_idss':city_name,
                   'area_id':area_name,
                   'searchtype':searchtype,
                   'keyword':filter_content,
                   'searchstatus':get_status,
                   'searchorder':get_searchorder,
                }
        response=redirect('/admin/shop_list/')
        response.set_cookie('data',data_dict,600)
        return response


def shop_edit(request):
    '''
   商户编辑
    '''
    if request.method=="GET":
        get_shop_id=int(request.GET.get('shop_id'))
        shop_obj=models.Shop.objects.filter(shop_id=get_shop_id).all()
        for i in shop_obj:
            region_obj = models.Region.objects.filter(region_id=i.region_id).first()
            province_obj = models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
            province_name = province_obj.site_name
            city_obj = models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
            city_name = city_obj.site_name
            area_obj = models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
            area_name = area_obj.site_name
            region_obj = models.Region.objects.filter(region_id=region_obj.region_id).first()
            shop_dict={
                'shop_id':get_shop_id,
                'shop_name':i.shop_name,
                'packing_commission':i.packing_commission,
                'phone_number':i.phone_number,
                'region_id':i.region_id,
                'status':i.status,
            }
            region_dict={
                'province_name': province_name,
                'city_name': city_name,
                'area_name': area_name,
                'region_name': region_obj.region_name,
            }
        return render(request,'Merchant/form.html',{'shop_dict':shop_dict,'region_dict':region_dict})
    if request.method=="POST":
        get_shop_id=request.POST.get('shop_id')
        get_name=request.POST.get('name')
        get_packing_commission=request.POST.get('Radios')
        get_phone_number=request.POST.get('phone')
        get_status=request.POST.get('options')
        get_region_id=request.POST.get('region_id')
        try:
            get_region_id=int(get_region_id)
        except ValueError:
            obj=models.Shop.objects.filter(shop_id=get_shop_id).first()
            get_region_id=obj.region_id
        models.Shop.objects.filter(shop_id=get_shop_id).update(
            shop_name=get_name,
            packing_commission=get_packing_commission,
            phone_number=get_phone_number,
            status=get_status,
            region_id=get_region_id,
        )
        return HttpResponse('修改成功')


def store_form(request):
    '''
    审核商店
    '''
    if request.method=="GET":
        get_shop_id=request.GET.get('shop_id')
        shop_obj=models.Shop.objects.filter(shop_id=get_shop_id).first()
        assistant_obj=models.ShopAssistant.objects.filter(shop_assistant_id=shop_obj.manager_id).first()
        region_obj=models.Region.objects.filter(region_id=shop_obj.region_id).first()
        province_obj=models.AddresLibrary.objects.filter(id=region_obj.province_id).first()
        city_obj=models.AddresLibrary.objects.filter(id=region_obj.city_id).first()
        area_obj=models.AddresLibrary.objects.filter(id=region_obj.area_id).first()
        province_name=province_obj.site_name
        city_name=city_obj.site_name
        area_name=area_obj.site_name
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
        if shop_obj.shop_logo:
            shop_logo = shop_obj.shop_logo.split('，')  # 商店logo地址列表
        else:
            shop_logo = []
        if shop_obj.business_license:
            business_license = shop_obj.business_license.split('，')  # 营业执照地址列表
        else:
            business_license = []
        if shop_obj.shop_photos:
            shop_photos = shop_obj.shop_photos.split('，')  # 商店场景图地址列表
        else:
            shop_photos = []
        if shop_obj.catering_license:
            catering_license = shop_obj.catering_license.split('，')  # 食品安全地址列表
        else:
            catering_license = []
        data={
            'shop_id':get_shop_id,
            'shop_name':shop_obj.shop_name,
            'shop_logo':shop_logo,
            'university_name':shop_obj.university_id,
            'campus_name':shop_obj.campus_id,
            'region_name':region_obj.region_name,
            'phone_number':shop_obj.phone_number,
            'manager_phone':assistant_obj.phone_number,
            'shop_type':shop_obj.shop_type,
            'in_area':province_name+city_name+area_name,
            'address':shop_obj.address,
            'business_license':business_license,
            'catering_license':catering_license,
            'bank_account':shop_obj.bank_account,
            'alipay_account':shop_obj.alipay_account,
            'shop_photos':shop_photos,#场景图
            'manage_name':assistant_obj.username,
        }
        return render(request,'Merchant/store_form.html',{'data':data})
    if request.method=="POST":
        get_shop_id=request.POST.get('shop_id')
        get_auth=request.POST.get('auth')
        get_remark=request.POST.get('remark')
        get_admin_name=request.session.get('user')
        get_admin_obj=models.Admin.objects.filter(account=get_admin_name).first()
        models.Shop.objects.filter(shop_id=get_shop_id).update(auth=get_auth)
        models.ShopAuditLog.objects.create(shop_id=get_shop_id,auth=get_auth,operator_id=get_admin_obj.id,remark=get_remark,create_time=timezone.now())
        return redirect('/admin/store_form/')


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
            x=json.loads(shop_obj.shop_photos)
            shop_obj.shop_photos=''
            for i in x:
                shop_obj.shop_photos+=i+'，'
        except Exception:
            pass
        try:
            x=json.loads(shop_obj.business_license)
            shop_obj.business_license=''
            for i in x:
                shop_obj.business_license+=i+'，'
        except Exception:
            pass
        if shop_obj.shop_logo:
            shop_logo = shop_obj.shop_logo.split('，')  # 商店logo地址列表
        else:
            shop_logo = []
        if shop_obj.business_license:
            business_license = shop_obj.business_license.split('，')  # 营业执照地址列表
        else:
            business_license = []
        if shop_obj.shop_photos:
            shop_photos = shop_obj.shop_photos.split('，')  # 商店场景图地址列表
        else:
            shop_photos = []
        if shop_obj.catering_license:
            catering_license = shop_obj.catering_license.split('，')  # 食品安全地址列表
        else:
            catering_license = []
        # shop_logo = shop_obj.shop_logo.split('，')  # logo地址列表
        # business_license = shop_obj.business_license.split('，')  # 营业执照地址列表
        # shop_photos = shop_obj.shop_photos.split('，')  # 商店展示地址列表
        data = {
            'shop_id': get_shop_id,
            'shop_name': shop_obj.shop_name,
            'shop_logo': shop_logo,
            'university_name': shop_obj.university_id,
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
            'alipay_account': shop_obj.alipay_account,
            'shop_photos': shop_photos,  # 场景图
            'manage_name': assistant_obj.username,
        }
        return render(request,'Merchant/status_form.html',{'data':data})


def fail_form(request):
    '''
    审核失败
    '''
    if request.method=='GET':
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
        if shop_obj.shop_logo:
            shop_logo = shop_obj.shop_logo.split('，')  # 商店logo地址列表
        else:
            shop_logo = []
        if shop_obj.business_license:
            business_license = shop_obj.business_license.split('，')  # 营业执照地址列表
        else:
            business_license = []
        if shop_obj.shop_photos:
            shop_photos = shop_obj.shop_photos.split('，')  # 商店场景图地址列表
        else:
            shop_photos = []
        if shop_obj.catering_license:
            catering_license = shop_obj.catering_license.split('，')  # 食品安全地址列表
        else:
            catering_license = []
        remark_obj=models.ShopAuditLog.objects.filter(shop_id=get_shop_id).first()
        data = {
            'shop_id': get_shop_id,
            'shop_name': shop_obj.shop_name,
            'shop_logo': shop_logo,
            'university_name': shop_obj.university_id,
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
            'alipay_account': shop_obj.alipay_account,
            'shop_photos': shop_photos,  # 场景图
            'manage_name': assistant_obj.username,
            'remark':remark_obj.remark,
        }
        return render(request, 'Merchant/fail_form.html', {'data': data})


def shop_delete(request):
    '''
   商户列表删除
    '''
    get_shop_id=request.GET.get('shop_id')
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
    if request.method=="GET":
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        get_pagesize=15
        get_page=request.GET.get('p','1')
        filter_content=request.GET.get('filter_content')
        if filter_content:
            if filter_content=='开启':
                status=1
            elif filter_content=='关闭':
                status = 0
            else:
                status=2
            try:
                filter_content=int(filter_content)
            except Exception:
                filter_content=filter_content
            if isinstance(filter_content,str):
                all_obj=models.Shop.objects.filter(Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj=models.Shop.objects.filter(Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            if obj.open_admin_region == 0:
                all_obj = all_obj.filter(auth=0)
            else:
                all_obj = all_obj.filter(auth=0, region_id=obj.open_admin_region)
        else:
            if obj.open_admin_region == 0:
                all_obj = models.Shop.objects.filter(auth=0).all()
            else:
                all_obj = models.Shop.objects.filter(auth=0, region_id=obj.open_admin_region).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list=[]
        for i in all_obj[start_nun:end_num]:
            data_dict={
                'shop_id':i.shop_id,
                'shop_name':i.shop_name,
                'phone_number':i.phone_number,
                'update_time':i.update_time,
                'status':i.status,
            }
            data_list.append(data_dict)
        return render(request,'Merchant/wait_store.html',{'data':data_list,'page_total':str(page_total),'get_page':get_page,'filter_content':filter_content})


def wait_store2(request):
    '''
    审核通过
    '''
    if request.method=="GET":
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        get_pagesize=15
        get_page=request.GET.get('p','1')
        filter_content=request.GET.get('filter_content')
        if filter_content:
            if filter_content=='开启':
                status=1
            elif filter_content=='关闭':
                status = 0
            else:
                status=2
            try:
                filter_content=int(filter_content)
            except Exception:
                filter_content=filter_content
            if isinstance(filter_content,str):
                all_obj=models.Shop.objects.filter(Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj=models.Shop.objects.filter(Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            if obj.open_admin_region == 0:
                all_obj = all_obj.filter(auth=2)
            else:
                all_obj = all_obj.filter(auth=2, region_id=obj.open_admin_region)
        else:
            if obj.open_admin_region == 0:
                all_obj = models.Shop.objects.filter(auth=2).all()
            else:
                all_obj = models.Shop.objects.filter(auth=2, region_id=obj.open_admin_region).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list=[]
        for i in all_obj[start_nun:end_num]:
            data_dict={
                'shop_id':i.shop_id,
                'shop_name':i.shop_name,
                'phone_number':i.phone_number,
                'update_time': i.update_time,
                'status':i.status,
            }
            data_list.append(data_dict)
        return render(request,'Merchant/wait_store_status.html',{'data':data_list,'page_total':str(page_total),'get_page':get_page,'filter_content':filter_content})


def wait_store3(request):
    '''
    审核失败
    '''
    if request.method=="GET":
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        get_pagesize=15
        get_page=request.GET.get('p','1')
        filter_content=request.GET.get('filter_content')
        if filter_content:
            if filter_content=='开启':
                status=1
            elif filter_content=='关闭':
                status = 0
            else:
                status=2
            try:
                filter_content=int(filter_content)
            except Exception:
                filter_content=filter_content
            if isinstance(filter_content,str):
                all_obj=models.Shop.objects.filter(Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            else:
                all_obj=models.Shop.objects.filter(Q(shop_id=filter_content) | Q(shop_name__contains=filter_content) | Q(phone_number__contains=filter_content) | Q(status=status))
            if obj.open_admin_region == 0:
                all_obj = all_obj.filter(auth=1)
            else:
                all_obj = all_obj.filter(auth=1, region_id=obj.open_admin_region)
        else:
            if obj.open_admin_region == 0:
                all_obj = models.Shop.objects.filter(auth=1).all()
            else:
                all_obj = models.Shop.objects.filter(auth=1, region_id=obj.open_admin_region).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list=[]
        for i in all_obj[start_nun:end_num]:
            data_dict={
                'shop_id':i.shop_id,
                'shop_name':i.shop_name,
                'phone_number':i.phone_number,
                'update_time': i.update_time,
                'status':i.status,
            }
            data_list.append(data_dict)
        return render(request,'Merchant/wait_store_fail.html',{'data':data_list,'page_total':str(page_total),'get_page':get_page,'filter_content':filter_content})


def category_list(request):
    '''
    分类列表
    '''
    get_pagesize=15
    get_page=request.GET.get('p','1')
    all_obj=models.ShopSort.objects.filter(parent_id=0).all()
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    if len(all_obj) % int(get_pagesize):
        page_total = len(all_obj) // int(get_pagesize) + 1
    else:
        page_total = len(all_obj) // int(get_pagesize)
    data_list=[]
    for i in all_obj.order_by('-priority')[start_nun:end_num]:
        data_dict = {
            'priority': i.priority,
            'sort_id': i.sort_id,
            'sort_name': i.sort_name,
            'status': i.state,
        }
        data_list.append(data_dict)
    return render(request,'Merchant/category_list.html',{'data':data_list,'page_total':str(page_total),'get_page':get_page})


def add_originalform(request):
    '''
   添加分类
    '''
    if request.method=="GET":
        return render(request, 'Merchant/add_originalform.html')
    if request.method=="POST":
        get_priority=request.POST.get('priority')
        get_sort_name=request.POST.get('sort_name')
        get_state=request.POST.get('state')
        models.ShopSort.objects.create(priority=get_priority,sort_name=get_sort_name,state=get_state,parent_id=0)
        return HttpResponse(1)


def edit_originalform(request):
    '''
    编辑分类
    '''
    if request.method=='GET':
        get_sort_id=request.GET.get('shop_id')
        obj=models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        data={
            'sort_id':get_sort_id,
            'sort_name':obj.sort_name,
            'priority':obj.priority,
            'state':obj.state
        }
        return render(request, 'Merchant/edit_originalform.html',{'data':data})
    elif request.method=='POST':
        get_sort_id=request.POST.get('sort_id')
        get_sort_name=request.POST.get('sort_name')
        get_priority=request.POST.get('priority')
        get_state=request.POST.get('state')
        models.ShopSort.objects.filter(sort_id=get_sort_id).update(sort_name=get_sort_name,priority=get_priority,state=get_state,parent_id=0)
        return HttpResponse(1)
    elif request.method=='DELETE':
        get_sort_id=request.GET.get('sort_id')
        models.ShopSort.objects.filter(sort_id=get_sort_id).delete()
        models.ShopSort.objects.filter(parent_id=get_sort_id).delete()
        return HttpResponse(1)


def check_childlist(request):
    '''
   子分类列表
    '''
    get_pagesize = 15
    get_page=request.GET.get('p','1')
    get_parent_name=request.GET.get('name')
    get_parent_id=request.GET.get('sort_id')
    all_obj=models.ShopSort.objects.filter(parent_id=get_parent_id).all()
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    if len(all_obj) % int(get_pagesize):
        page_total = len(all_obj) // int(get_pagesize) + 1
    else:
        page_total = len(all_obj) // int(get_pagesize)
    data_list=[]
    for i in all_obj.order_by('priority')[start_nun:end_num]:
        data_dict={}
        data_dict['sort_id']=i.sort_id
        data_dict['sort_name']= i.sort_name
        data_dict['priority']= i.priority
        data_dict['state']= i.state
        data_list.append(data_dict)
    return render(request, 'Merchant/category_childlist.html',{'data':data_list,'f_id':get_parent_id,'name':get_parent_name,'page_total':str(page_total),'get_page':get_page})


def add_childform(request):
    '''
    添加子分类
    '''
    if request.method=='GET':
        parent_id=request.GET.get("shop_id")
        return render(request, 'Merchant/add_childform.html',{'parent_id':parent_id})
    elif request.method=='POST':
        get_parent_id=request.POST.get('parent_id')
        get_sort_name=request.POST.get('sort_name')
        get_priority=request.POST.get('priority')
        get_state=request.POST.get('state')
        models.ShopSort.objects.create(parent_id=get_parent_id,sort_name=get_sort_name,state=get_state,priority=get_priority)
        return HttpResponse(1)


def edit_childform(request):
    '''
    编辑子分类
    '''
    if request.method=='GET':
        get_sort_id=request.GET.get('shop_id')
        obj=models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        data={
            'sort_id':get_sort_id,
            'sort_name':obj.sort_name,
            'priority':obj.priority,
            'state':obj.state
        }
        return render(request, 'Merchant/edit_childlform.html',{'data':data})
    elif request.method=='POST':
        get_sort_id=request.POST.get('sort_id')
        parent_obj=models.ShopSort.objects.filter(sort_id=get_sort_id).first()
        obj=models.ShopSort.objects.filter(sort_id=parent_obj.parent_id).first()
        get_sort_name=request.POST.get('sort_name')
        get_priority=request.POST.get('priority')
        get_state=request.POST.get('state')
        models.ShopSort.objects.filter(sort_id=get_sort_id).update(sort_name=get_sort_name,priority=get_priority,state=get_state,parent_id=parent_obj.parent_id)
        url='/admin/check_childlist/?sort_id='+str(parent_obj.parent_id)+"&name="+obj.sort_name
        return redirect(url)
    elif request.method=='DELETE':
        get_sort_id=request.GET.get('sort_id')
        models.ShopSort.objects.filter(sort_id=get_sort_id).delete()
        return HttpResponse(1)


def account_list(request):
    '''
    管理员列表
    '''
    get_pagesize=15
    get_page=request.GET.get('p','1')
    get_account = request.session['user']
    obj = models.Admin.objects.filter(account=get_account).first()
    get_level = obj.level
    if get_level==0:
        all_obj=models.Admin.objects.filter(level__lt=2).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj.order_by('level')[start_nun:end_num]:
            region_obj=models.Region.objects.filter(region_id=i.open_admin_region).first()
            if not region_obj:
                region_name='平台所有区域'
            else:
                region_name=region_obj.region_name
            data_dict={
                'id':i.id,
                'account':i.account,
                'realname':i.realname,
                'phone':i.phone,
                'email':i.email,
                'qq':i.qq,
                'last_ip':i.last_ip,
                'last_time':i.last_time,
                'login_count':i.login_count,
                'status': i.status,
                'level':i.level,
                'nickname':i.nickname,
                'open_admin_region':region_name,
            }
            data_list.append(data_dict)
    if get_level==1:
        all_obj = models.Admin.objects.filter(level=2,open_admin_region=obj.open_admin_region).all()
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
    return render(request, 'Index/account.html',{'data':data_list,'get_page':get_page,'page_total':str(page_total)})


def authority_group(request):

    return render(request, 'Index/authority_group.html')


def add_account(request):
    '''
    添加管理员
    '''
    if request.method=='GET':
        operate_name = request.session.get('user')
        obj = models.Admin.objects.filter(account=operate_name).first()
        operate_level = obj.level
        operate_region = obj.open_admin_region
        return render(request, 'Index/add_accountform.html',{'level':operate_level,'region_id':operate_region})
    elif request.method=='POST':
        get_operator=request.session.get('user')
        operator_obj=models.Admin.objects.filter(account=get_operator).first()
        get_account=request.POST.get('account')
        get_pwd=request.POST.get('pwd')
        get_realname=request.POST.get('realname')
        get_phone=request.POST.get('phone')
        get_email=request.POST.get('email')
        get_qq=request.POST.get('qq')
        get_level=request.POST.get('level')
        get_region=request.POST.get('region_id')
        if get_region:
            get_region=get_region
        else:
            if get_level=='2':
                operate_name = request.session.get('user')
                obj = models.Admin.objects.filter(account=operate_name).first()
                get_region=obj.open_admin_region
            else:
                get_region=0
        get_menus=request.POST.get('authoritydata')
        get_menus=get_menus.split(',')
        all_obj=models.Menu.objects.filter(field_function_name__in=get_menus).exclude(parent_id=0)
        parent_list=[]
        for i in all_obj:
            if i.parent_id not in parent_list:
                parent_list.append(i.parent_id)
        data_list=[]
        for i in parent_list:
            parent_dict={}
            son_list=[]
            for j in all_obj.filter(parent_id=i).all():
                son_list.append(j.id)
            parent_dict[i]=son_list
            data_list.append(parent_dict)
        if not data_list:data_list=json.loads(operator_obj.menus)
        data_list=json.dumps(data_list)
        models.Admin.objects.create(account=get_account,pwd=get_pwd,realname=get_realname,phone=get_phone,email=get_email,qq=get_qq,login_count=0,status=1,level=get_level,open_admin_region=get_region,menus=data_list,last_time=timezone.now())
        return HttpResponse(2)


def permissions(request):
    '''
    显示能够赋予权限
    '''
    if request.method=='GET':
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
        return JsonResponse(data_list,safe=False)


def account_unique(request):
    get_account=request.GET.get('account')
    if models.Admin.objects.filter(account=get_account):
        return JsonResponse({'state':1})
    else:
        return JsonResponse({'state':0})


def edit_accountinfo(request):
    if request.method=='GET':
        get_parent=request.session.get('user')
        parent_obj=models.Admin.objects.filter(account=get_parent).first()
        get_admin_id=request.GET.get('shop_id')
        obj=models.Admin.objects.filter(id=get_admin_id).first()
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
                'city_name':'',
                'area_name': '',
                'region_name':'',
            }

        return render(request, 'Index/edit_accountinfo.html',{'data':data,'parent_level':parent_obj.level})
    elif request.method=='POST':
        get_account = request.POST.get('account')
        get_pwd = request.POST.get('pwd')
        get_realname = request.POST.get('realname')
        get_phone = request.POST.get('phone')
        get_email = request.POST.get('email')
        get_qq = request.POST.get('qq')
        get_level = request.POST.get('level')
        get_region = request.POST.get('region_id')
        if get_level==0:
            get_region=0
        elif get_level==1:
            get_region = get_region
        else:
            operate_name = request.session.get('user')
            obj = models.Admin.objects.filter(account=operate_name).first()
            get_region = obj.open_admin_region
        if get_pwd:
            models.Admin.objects.filter(account=get_account).update(pwd=get_pwd,realname=get_realname,phone=get_phone,email=get_email,qq=get_qq,level=get_level,open_admin_region=get_region)
        else:
            models.Admin.objects.filter(account=get_account).update(realname=get_realname,phone=get_phone,email=get_email,qq=get_qq,level=get_level,open_admin_region=get_region)
        return redirect('/admin/account_list/')
    elif request.method=='DELETE':
        get_id=request.GET.get('account_id')
        models.Admin.objects.filter(id=get_id).delete()
        return HttpResponse(0)


def edit_authorityform(request):
    get_id=request.GET.get('shop_id')
    obj=models.Admin.objects.filter(id=get_id).first()
    obj_list=[]
    for i in json.loads(obj.menus):
        for key,val in i.items():
            obj_list.append(key)
            for j in val:
                obj_list.append(j)
    data_list=[]
    for i in obj_list:
        permission_name=models.Menu.objects.filter(id=i).values_list('field_function_name')[0][0]
        data_list.append(permission_name)
    print(data_list)
    return render(request, 'Index/edit_authorityform.html',{'data':data_list})

def test(request):
    return render(request,'Merchant/form.html')
















