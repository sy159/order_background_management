from django.shortcuts import render, redirect, HttpResponse
from orange_manage import models
from django.utils import timezone


def recommend_list(request):
    if request.method == 'GET':
        if request.operator_region:
            all_obj = models.RecommendShops.objects.filter(region_id=request.operator_region)
        else:
            all_obj = models.RecommendShops.objects.all()
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj.order_by('-priority')[start_nun:end_num]:
            data_dict = {
                'id': i.id,
                'shop_name': i.shop_name,
                'priority': i.priority,
                'operator': i.operator_name,
                'last_time': i.last_time,
                'status': i.status,
                'img': request.FTP_HOST + request.recommend_shops_images + i.img,
            }
            data_list.append(data_dict)
        return render(request, 'Promotion_market/recommend_list.html',
                      {'data': data_list, 'get_page': int(get_page), 'page_total': page_total})
    elif request.method == 'DELETE':
        get_id = request.GET.get('id')
        models.RecommendShops.objects.filter(id=get_id).delete()
        return HttpResponse(1)


def store_add(request):
    if request.method == 'GET':
        return render(request, 'Promotion_market/store_add.html')
    elif request.method == 'POST':
        get_shop_id = request.POST.get('get_url').split('=')[1]
        get_img = request.POST.get('img')
        get_hiddenstore = request.POST.get('hiddenstore')
        get_sort = request.POST.get('sort')
        get_status = request.POST.get('status')
        data = {
            'shop_id': get_shop_id,
            'shop_name': get_hiddenstore,
            'priority': get_sort,
            'operator_name': request.operator_name,
            'status': get_status,
            'operator_id': request.operator_id,
            'img': get_img,
            'region_id': request.operator_region,
            'last_time': timezone.now(),
        }
        models.RecommendShops.objects.create(**data)
        return HttpResponse(1)


def store_edit(request):
    if request.method == 'GET':
        get_id = request.GET.get('id')
        obj = models.RecommendShops.objects.get(id=get_id)
        data_dict = {
            'id': obj.id,
            'shop_name': obj.shop_name,
            'priority': obj.priority,
            'status': obj.status,
            'img': request.FTP_HOST + request.recommend_shops_images + obj.img,
        }
        return render(request, 'Promotion_market/store_edit.html', {'data': data_dict})
    elif request.method == 'POST':
        get_id = request.POST.get('store_id')
        obj = models.RecommendShops.objects.get(id=get_id)
        img = request.POST.get('img') if len(request.POST.get('img')) else obj.img
        data_dict = {
            'img': img,
            'status': request.POST.get('status'),
            'priority': request.POST.get('sort'),
        }
        models.RecommendShops.objects.filter(id=get_id).update(**data_dict)
        return HttpResponse(1)


def coupon_list(request):
    if request.method == 'GET':
        get_pagesize = 15
        get_page = request.GET.get('p', '1')
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        all_obj = models.Coupon.objects.all()
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            details = ''
            if i.coupon_type == 2:
                details = str(i.coupon_value) + '元现金券'
            elif i.coupon_type == 1:
                details = '满' + str(i.use_condition) + '元打' + str(i.coupon_value) + '折'
            elif i.coupon_type == 0:
                details = '满' + str(i.use_condition) + '元减' + str(i.coupon_value) + '元'
            shop_classify = ''
            goods_classify = ''
            for j in eval(i.shop_classify):
                if j == 0:
                    shop_classify = '平台所有'
                else:
                    obj = models.ShopCategory.objects.get(id=j)
                    shop_classify += obj.name + ' '
            for g in eval(i.goods_classify):
                if g == 0:
                    goods_classify = '平台所有'
                else:
                    g_obj = models.GoodsClassifyPlatform.objects.get(record_id=g)
                    goods_classify += g_obj.name + ' '
            data_dict = {
                'coupon_id': i.coupon_id,
                'coupon_name': i.coupon_name,  # 优惠券名称
                'image': request.FTP_HOST + request.coupon_images + str(i.image),  # 优惠券图片
                'shop_classify': shop_classify,
                'goods_classify': goods_classify,
                'publish_amount': i.publish_amount,  # 发行的总数，-1为无限
                'spare_amount': i.spare_amount,  # 已领取数量
                # 'spar_amount': i.spare_amount,  # 已使用数量 todo
                'start_time': i.start_time,  # 开始时间
                'end_time': i.end_time,  # 结束时间
                'details': details,  # 优惠详情
                'status': i.status,  # 指商户是否发行，已领取用户无影响
                'just_newuser': i.just_newuser,  # 是否新用户
            }
            data_list.append(data_dict)
        return render(request, 'Promotion_market/PlatformCoupons.html',
                      {'data': data_list, 'get_page': int(get_page), 'page_total': page_total})


def add_coupon(request):
    if request.method == 'POST':
        try:
            if request.POST.get('coupon_type') == '1':
                coupon_type = 1
            else:
                coupon_type = 2 if request.POST.get('use_condition') == '0' else 0
            get_goods_classify2 = request.POST.get('goods_classify2')
            get_goods_classify1 = request.POST.get('goods_classify1')
            goods_classify = get_goods_classify2 if get_goods_classify2 != '0' else get_goods_classify1
            end_time = request.POST.get('end_time') if request.POST.get('end_time') else None
            shop_classify_list = []
            shop_classify_list.append(int(request.POST.get('shop_classify')))
            goods_classify_list = []
            goods_classify_list.append(int(goods_classify))
            data = {
                'coupon_name': request.POST.get('coupon_name'),
                'image': request.POST.get('img'),
                'shop_id': 0,  # 平台添加为0
                'coupon_type': coupon_type,  # 优惠券类型
                'use_condition': request.POST.get('use_condition'),  # 优惠券使用条件
                'coupon_value': request.POST.get('coupon_value'),  # 优惠券减免数量
                'description': request.POST.get('description'),  # 描述
                'publish_amount': request.POST.get('publish_amount'),  # 发行数量
                'status': request.POST.get('status'),
                'create_time': timezone.now(),  # 创建时间
                'superposable': request.POST.get('superposable'),  # 是否可叠加使用
                'start_time': request.POST.get('start_time'),  # 优惠券发行开始时间
                'end_time': end_time,  # 优惠券结束发行时间  为 null 指无期限发行
                'just_newuser': request.POST.get('just_newuser'),  # 是否新用户
                'shop_classify': shop_classify_list,  # 平台店铺分类id list
                'goods_classify': goods_classify_list,  # 平台商品分类id list
            }
            models.Coupon.objects.create(**data)
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)
    shop_obj = models.ShopCategory.objects.all()
    goods_obj = models.GoodsClassifyPlatform.objects.filter(parent_id=-1)
    shop_data = []
    goods_data = []
    for i in shop_obj:
        shop_list = []
        shop_list.append(i.id)
        shop_list.append(i.name)
        shop_data.append(shop_list)
    for i in goods_obj:
        goods_list = []
        goods_list.append(i.record_id)
        goods_list.append(i.name)
        goods_data.append(goods_list)
    return render(request, 'Promotion_market/coupons_add.html', {'shop_data': shop_data, 'goods_data': goods_data})


def edit_coupon(request):
    if request.method == 'GET':
        get_coupon_id = request.GET.get('coupon_id')
        obj = models.Coupon.objects.get(coupon_id=get_coupon_id)
        if eval(obj.goods_classify)[0] == 0:
            goods_classify1 = eval(obj.goods_classify)[0]
            goods_classify2 = '0'
        else:
            goods_obj = models.GoodsClassifyPlatform.objects.get(record_id=eval(obj.goods_classify)[0])
            if goods_obj.parent_id != -1:
                g_obj = models.GoodsClassifyPlatform.objects.get(record_id=goods_obj.parent_id)
                goods_classify1 = g_obj.record_id
                goods_classify2 = eval(obj.goods_classify)[0]
            else:
                goods_classify1 = eval(obj.goods_classify)[0]
                goods_classify2 = 0
        data = {
            'coupon_id': get_coupon_id,
            'coupon_name': obj.coupon_name,
            'image': request.FTP_HOST + request.coupon_images + obj.image,
            'coupon_type': obj.coupon_type,  # 优惠券类型
            'use_condition': obj.use_condition,  # 优惠券使用条件
            'coupon_value': obj.coupon_value,  # 优惠券减免数量
            'description': obj.description,  # 描述
            'publish_amount': obj.publish_amount,  # 发行数量
            'status': obj.status,
            'superposable': obj.superposable,  # 是否可叠加使用
            'start_time': obj.start_time,  # 优惠券发行开始时间
            'end_time': obj.end_time,  # 优惠券结束发行时间  为 null 指无期限发行
            'just_newuser': obj.just_newuser,  # 是否新用户
            'shop_classify': obj.shop_classify,  # 平台店铺分类id list
            'goods_classify1': goods_classify1,  # 平台商品分类id list
            'goods_classify2': goods_classify2,  # 平台商品分类id list
        }
        shop_obj = models.ShopCategory.objects.all()
        goods_obj = models.GoodsClassifyPlatform.objects.filter(parent_id=-1)
        shop_data = []
        goods_data = []
        for i in shop_obj:
            shop_list = []
            shop_list.append(str(i.id))
            shop_list.append(i.name)
            shop_data.append(shop_list)
        for i in goods_obj:
            goods_list = []
            goods_list.append(i.record_id)
            goods_list.append(i.name)
            goods_data.append(goods_list)
        return render(request, 'Promotion_market/coupons_edit.html',
                      {'data': data, 'shop_data': shop_data, 'goods_data': goods_data})
    elif request.method == 'POST':
        try:
            if request.POST.get('coupon_type') == '1':
                coupon_type = 1
            else:
                coupon_type = 2 if request.POST.get('use_condition') == '0' else 0
            get_goods_classify2 = request.POST.get('goods_classify2')
            get_goods_classify1 = request.POST.get('goods_classify1')
            goods_classify = get_goods_classify2 if get_goods_classify2 != '0' else get_goods_classify1
            end_time = request.POST.get('end_time') if request.POST.get('end_time') else None
            shop_classify_list = []
            shop_classify_list.append(int(request.POST.get('shop_classify')))
            goods_classify_list = []
            goods_classify_list.append(int(goods_classify))
            if request.POST.get('img'):
                data = {
                    'coupon_name': request.POST.get('coupon_name'),
                    'image': request.POST.get('img'),
                    'coupon_type': coupon_type,  # 优惠券类型
                    'use_condition': request.POST.get('use_condition'),  # 优惠券使用条件
                    'coupon_value': request.POST.get('coupon_value'),  # 优惠券减免数量
                    'description': request.POST.get('description'),  # 描述
                    'publish_amount': request.POST.get('publish_amount'),  # 发行数量
                    'status': request.POST.get('status'),
                    'create_time': timezone.now(),  # 创建时间
                    'superposable': request.POST.get('superposable'),  # 是否可叠加使用
                    'start_time': request.POST.get('start_time'),  # 优惠券发行开始时间
                    'end_time': end_time,  # 优惠券结束发行时间  为 null 指无期限发行
                    'just_newuser': request.POST.get('just_newuser'),  # 是否新用户
                    'shop_classify': shop_classify_list,  # 平台店铺分类id list
                    'goods_classify': goods_classify_list,  # 平台商品分类id list
                }
            else:
                data = {
                    'coupon_name': request.POST.get('coupon_name'),
                    'coupon_type': coupon_type,  # 优惠券类型
                    'use_condition': request.POST.get('use_condition'),  # 优惠券使用条件
                    'coupon_value': request.POST.get('coupon_value'),  # 优惠券减免数量
                    'description': request.POST.get('description'),  # 描述
                    'publish_amount': request.POST.get('publish_amount'),  # 发行数量
                    'status': request.POST.get('status'),
                    'create_time': timezone.now(),  # 创建时间
                    'superposable': request.POST.get('superposable'),  # 是否可叠加使用
                    'start_time': request.POST.get('start_time'),  # 优惠券发行开始时间
                    'end_time': end_time,  # 优惠券结束发行时间  为 null 指无期限发行
                    'just_newuser': request.POST.get('just_newuser'),  # 是否新用户
                    'shop_classify': shop_classify_list,  # 平台店铺分类id list
                    'goods_classify': goods_classify_list,  # 平台商品分类id list
                }
            models.Coupon.objects.filter(coupon_id=request.POST.get('coupon_id')).update(**data)
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)
