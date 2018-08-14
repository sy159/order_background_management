from django.shortcuts import render, HttpResponse, redirect
from orange_manage import models
from django.utils import timezone


def adver_management(request):
    return render(request, 'Adver/adver_management.html')


def adver_list(request):
    if request.method == 'GET':
        operator_region = request.operator_region
        get_id = request.GET.get('id')
        if get_id == '1':
            if operator_region == 0:
                all_obj = models.Banner.objects.all()
            else:
                all_obj = models.Banner.objects.filter(region_id=operator_region).all()
            data_list = []
            for i in all_obj.order_by('-priority'):
                try:
                    url_type = i.url.split("=")[1].split("#")[0]
                    url_id = i.url.split("#")[1]
                    if url_type == 'shop':
                        shop_obj = models.Shop.objects.filter(shop_id=url_id).first()
                        url_name = '店铺:' + shop_obj.shop_name if shop_obj else '店铺不存在'
                    else:
                        goods_obj = models.Goods.objects.filter(goods_id=url_id).first()
                        if goods_obj:
                            shop_obj = models.Shop.objects.filter(shop_id=goods_obj.shop_id).first()
                            url_name = '店铺:' + shop_obj.shop_name + ' 商品:' + goods_obj.goods_name
                        else:
                            url_name = '商品不存在'
                except Exception:
                    url_name = i.url
                data_dict = {
                    'id': i.id,
                    'priority': i.priority,
                    'region_id': i.region_id,
                    'title': i.title,
                    'img': request.FTP_HOST + request.banner_images + i.img,
                    'url': url_name,
                    'state': i.state,
                    'start': i.start,
                    'end': i.end,
                    'has_prescription': i.has_prescription,
                }
                data_list.append(data_dict)
            return render(request, 'Adver/adver_list.html',
                          {'data': data_list, 'parent_title': 'App首页轮播图', 'parent_id': get_id})
        elif get_id == '2':
            if operator_region == 0:
                all_obj = models.AppMenu.objects.all()
            else:
                all_obj = models.AppMenu.objects.filter(region_id=operator_region).all()
            data_list = []
            for i in all_obj.order_by('-priority'):
                try:
                    url_type = i.url.split("=")[1].split("#")[0]
                    url_id = i.url.split("#")[1]
                    if url_type == 'shop':
                        shop_obj = models.Shop.objects.filter(shop_id=url_id).first()
                        url_name = '店铺:' + shop_obj.shop_name if shop_obj else '店铺不存在'
                    else:
                        goods_obj = models.Goods.objects.filter(goods_id=url_id).first()
                        if goods_obj:
                            shop_obj = models.Shop.objects.filter(shop_id=goods_obj.shop_id).first()
                            url_name = '店铺:' + shop_obj.shop_name + ' 商品:' + goods_obj.goods_name
                        else:
                            url_name = '商品不存在'
                except Exception:
                    url_name = i.url
                data_dict = {
                    'id': i.id,
                    'priority': i.priority,
                    'region_id': i.region_id,
                    'title': i.title,
                    'img': request.FTP_HOST + request.app_menu_images + i.img,
                    'url': url_name,
                    'state': i.state,
                }
                data_list.append(data_dict)
            return render(request, 'Adver/adver_list.html',
                          {'data': data_list, 'parent_title': 'App首页菜单', 'parent_id': get_id})
    elif request.method == 'DELETE':
        get_parent_id = request.GET.get('parent_id')
        get_id = request.GET.get('adver_id')
        if get_parent_id == '1':
            models.Banner.objects.filter(id=get_id).delete()
        elif get_parent_id == '2':
            models.AppMenu.objects.filter(id=get_id).delete()
        return HttpResponse(1)


def adver_add(request):
    if request.method == 'GET':
        get_id = request.GET.get('parent_id')
        return render(request, 'Adver/adver_add.html', {'parent_id': get_id})
    elif request.method == 'POST':
        get_id = request.GET.get('parent_id')
        operator_region = request.operator_region
        get_title = request.POST.get("adver_name")
        get_status = request.POST.get("status")
        get_img = request.POST.get("img")
        get_priority = request.POST.get("sort")
        get_url = request.POST.get("get_url")  # 获取格式为shop_id=9或者goods_id=9
        if request.POST.get('function') == '2':
            get_url = request.POST.get('url')
        else:
            get_url = '?a=shop#' + get_url.split('=')[1] if 'shop' in get_url else '?a=goods#' + get_url.split('=')[1]
        if get_id == '1':
            models.Banner.objects.create(title=get_title, img=get_img, url=get_url, priority=get_priority,
                                         state=get_status, region_id=operator_region)
        elif get_id == '2':
            models.AppMenu.objects.create(title=get_title, img=get_img, url=get_url, priority=get_priority,
                                          state=get_status, region_id=operator_region)
        return HttpResponse(1)


def stores(request):
    get_flag = request.GET.get('flag')
    operator_region = request.operator_region
    if request.method == 'GET':
        get_page = request.GET.get('p', '1')
        get_pagesize = 5
        get_search_content = request.GET.get('keyword')
        if get_search_content:
            if operator_region == 0:
                all_obj = models.Shop.objects.filter(auth=2, status=1,
                                                     shop_name__contains=get_search_content).all()  # 审核通过，状态开启
            else:
                all_obj = models.Shop.objects.filter(auth=2, status=1, region_id=operator_region,
                                                     shop_name__contains=get_search_content).all()  # 审核通过，状态开启
        else:
            if operator_region == 0:
                all_obj = models.Shop.objects.filter(auth=2, status=1).all()  # 审核通过，状态开启
            else:
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
        return render(request, 'Adver/stores.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total), 'flag': get_flag, })


def goods(request):
    get_shop_id = request.GET.get('shop_id')
    get_stores = request.GET.get('stores')
    if request.method == 'GET':
        get_pagesize = 5
        get_page = request.GET.get('p', '1')
        get_search_content = request.GET.get('keyword')
        if get_search_content:
            all_obj = models.Goods.objects.filter(shop_id=get_shop_id, goods_name__contains=get_search_content).all()
        else:
            all_obj = models.Goods.objects.filter(shop_id=get_shop_id).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'goods_id': i.goods_id,
                'goods_name': i.goods_name,
            }
            data_list.append(data_dict)
        return render(request, 'Adver/goods.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total), 'stores': get_stores,
                       'shop_id': get_shop_id})


def adver_edit(request):
    if request.method == 'GET':
        get_parent_id = request.GET.get('parent_id')
        get_adver_id = request.GET.get('adver_id')
        if get_parent_id == '1':  # 首页轮播
            obj = models.Banner.objects.filter(id=get_adver_id).first()
            img = request.FTP_HOST + request.banner_images + obj.img
        elif get_parent_id == '2':  # 菜单
            obj = models.AppMenu.objects.filter(id=get_adver_id).first()
            img = request.FTP_HOST + request.app_menu_images + obj.img
        data_dict = {
            'adver_id': get_adver_id,
            'title': obj.title,
            'img': img,
            'priority': obj.priority,
            'state': obj.state
        }
        return render(request, 'Adver/adver_edit.html', {'data': data_dict, 'parent_id': get_parent_id})
    elif request.method == 'POST':
        get_parent_id = request.POST.get('parent_id')
        get_shop_id = request.POST.get('adver_id')
        if get_parent_id == '1':  # 轮播图
            obj = models.Banner.objects.filter(id=get_shop_id).first()
        elif get_parent_id == '2':  # 菜单栏
            obj = models.AppMenu.objects.filter(id=get_shop_id).first()
        get_title = request.POST.get('name')
        get_status = request.POST.get('status')
        get_img = request.POST.get('img')
        get_priority = request.POST.get('sort')
        get_url = request.POST.get('get_url')  # 获取格式为shop_id=9或者goods_id=9
        if not len(get_title): get_title = obj.title
        if not len(get_status): get_status = obj.state
        if not len(get_img): get_img = obj.img
        if not len(get_priority): get_priority = obj.priority
        if request.POST.get('function') == '2':
            url = request.POST.get('url')
            if 'http://' in url or 'https://' in url:
                get_url = url
            else:
                get_url = 'http://' + url
        elif request.POST.get('function') == '1':
            if not len(get_url): get_url = obj.url.split('=')[1].split('#')[0] + '=' + obj.url.split('=')[1].split('#')[
                1]
            get_url = '?a=shop#' + get_url.split('=')[1] if 'shop' in get_url else '?a=goods#' + get_url.split('=')[1]
        else:
            get_url = obj.url
        if get_parent_id == '1':  # 轮播图
            models.Banner.objects.filter(id=get_shop_id).update(title=get_title, img=get_img, url=get_url,
                                                                state=get_status, priority=get_priority)
        elif get_parent_id == '2':  # 菜单栏
            models.AppMenu.objects.filter(id=get_shop_id).update(title=get_title, img=get_img, url=get_url,
                                                                 state=get_status, priority=get_priority)
        return HttpResponse(1)


def withdraw_list(request):
    if request.method == 'GET':
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if request.operator_region:
            all_obj = models.CashApplications.objects.filter(region_id=request.operator_region)
        else:
            all_obj = models.CashApplications.objects.all()
        status_dict = {
            'keyword': request.GET.get('keyword'),
            'searchtype': request.GET.get('searchtype'),
            'status': request.GET.get('status'),
            'cash_account_type': request.GET.get('cash_account_type'),
            'identity': request.GET.get('identity'),
        }
        if request.GET.get('keyword'):
            if request.GET.get('searchtype') == 'account_phone':
                all_obj = all_obj.filter(account_phone__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'account_holder':
                all_obj = all_obj.filter(account_holder__contains=request.GET.get('keyword'))
        if request.GET.get('status'): all_obj = all_obj.filter(status=request.GET.get('status'))
        if request.GET.get('cash_account_type'): all_obj = all_obj.filter(
            cash_account_type=request.GET.get('cash_account_type'))
        if request.GET.get('identity'): all_obj = all_obj.filter(identity=request.GET.get('identity'))
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj.order_by('-amount')[start_nun:end_num]:
            data_dict = {
                'id': i.id,
                'identity': i.identity,  # 提现用户角色; 1:user 2:shopAssistant 3:distributor
                'account_id': i.account_id,
                'account_phone': i.account_phone,  # 账户电话
                'cash_account_type': i.cash_account_type,  # 提现目标账户类型: 1:支付宝 2:微信 3:银行账户
                'cash_account': i.cash_account,  # 提现目标账号
                'account_holder': i.account_holder,  # 提款人真实姓名
                'bank_name': i.bank_name,  # 提款银行
                'amount': i.amount,  # 提款金额
                'create_time': i.create_time,  # 申请时间
                'payment_time': i.payment_time,  # 转账时间
                'status': i.status,  # 状态 0:未审核，1:审核通过，2:已打款，3:审核失败
            }
            data_list.append(data_dict)
        return render(request, 'System_Setting/withdraw_auto.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'status_dict': status_dict})
    elif request.method == 'POST':
        get_id = request.POST.get('id')
        get_status = request.POST.get('status')
        models.CashApplications.objects.filter(id=get_id).update(status=get_status)
        return HttpResponse(1)


def modify_status(request):
    if request.method == 'GET':
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        all_obj = models.CashApplications.objects.filter(status=1)
        if request.operator_region: all_obj = all_obj.filter(region_id=request.operator_region)
        status_dict = {
            'keyword': request.GET.get('keyword'),
            'searchtype': request.GET.get('searchtype'),
            'status': request.GET.get('status'),
            'cash_account_type': request.GET.get('cash_account_type'),
            'identity': request.GET.get('identity'),
        }
        if request.GET.get('keyword'):
            if request.GET.get('searchtype') == 'account_phone':
                all_obj = all_obj.filter(account_phone__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'account_holder':
                all_obj = all_obj.filter(account_holder__contains=request.GET.get('keyword'))
            elif request.GET.get('searchtype') == 'id':
                all_obj = all_obj.filter(id=request.GET.get('keyword'))
        if request.GET.get('cash_account_type'): all_obj = all_obj.filter(
            cash_account_type=request.GET.get('cash_account_type'))
        if request.GET.get('identity'): all_obj = all_obj.filter(identity=request.GET.get('identity'))
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj.order_by('-amount')[start_nun:end_num]:
            data_dict = {
                'id': i.id,
                'identity': i.identity,  # 提现用户角色; 1:user 2:shopAssistant 3:distributor
                'account_id': i.account_id,
                'account_phone': i.account_phone,  # 账户电话
                'cash_account_type': i.cash_account_type,  # 提现目标账户类型: 1:支付宝 2:微信 3:银行账户
                'cash_account': i.cash_account,  # 提现目标账号
                'account_holder': i.account_holder,  # 提款人真实姓名
                'bank_name': i.bank_name,  # 提款银行
                'amount': i.amount,  # 提款金额
                'create_time': i.create_time,  # 申请时间
                'payment_time': i.payment_time,  # 转账时间
                'status': i.status,  # 状态 0:未审核，1:审核通过，2:已打款，3:审核失败
            }
            data_list.append(data_dict)
        return render(request, 'System_Setting/ModifyPaymentStatus.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'status_dict': status_dict})
    elif request.method == 'POST':
        try:
            get_id = request.POST.get('id')
            data = {
                'status': 2,
                'operator_id': request.operator_id,
                'operator_name': request.operator_name,
                'operator_phone': request.operator_obj.phone,
                'payment_time': timezone.now(),
            }
            models.CashApplications.objects.filter(id=get_id).update(**data)
            return HttpResponse(1)
        except Exception:
            return HttpResponse(0)
