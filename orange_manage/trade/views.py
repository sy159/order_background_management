from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum, Q, F
from orange_manage import models


def order_list(request):
    get_pagesize = 15
    get_page = request.GET.get('p', '1')
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    get_keyword = request.GET.get('keyword', '')
    get_searchtype = request.GET.get('searchtype', 'order_id')
    get_begin_time = request.GET.get('begin_time', '')
    get_end_time = request.GET.get('end_time', '')
    get_order_status = request.GET.get('order_status', '-1')
    get_payment = request.GET.get('payment', '3')
    search_data = {
        'keyword': get_keyword,
        'begin_time': get_begin_time,
        'searchtype': get_searchtype,
        'end_time': get_end_time,
        'order_status': get_order_status,
        'payment': get_payment,
    }
    if request.operator_region:
        all_obj = models.Orders.objects.filter(order_status__isnull=False,
                                               region_id=request.operator_region).order_by("-create_time").all()
    else:
        all_obj = models.Orders.objects.filter(order_status__isnull=False).order_by("-create_time").all()
    if get_keyword:
        if get_searchtype == 'order_id':
            all_obj = all_obj.filter(order_id__contains=get_keyword)
        elif get_searchtype == 'user_name':
            all_obj = all_obj.filter(user_name__contains=get_keyword)
        elif get_searchtype == 'user_phone_number':
            all_obj = all_obj.filter(user_phone_number__contains=get_keyword)
    if get_begin_time and get_end_time:
        all_obj = all_obj.filter(create_time__gte=get_begin_time)
        all_obj = all_obj.filter(create_time__lte=get_end_time)
    if get_order_status != '-1' and get_order_status:
        all_obj = all_obj.filter(order_status=get_order_status)
    if get_payment != '3':
        all_obj = all_obj.filter(pay_mode=get_payment)
    page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
        get_pagesize)
    data_list = []
    for i in all_obj[start_nun:end_num]:
        data_dict = {
            'order_id': i.order_id,
            'order_status': i.order_status,
            'user_name': i.user_name,
            'user_phone_number': i.user_phone_number,
            'total_price': i.total_price,
            'pay_time': i.pay_time,
            'complete_time': i.complete_time,
            'pay_mode': i.pay_mode,
        }
        data_list.append(data_dict)
    if request.operator_region == 0:
        unpaid = models.OrderStatusLogs.objects.aggregate(all_num=Sum('unpaid'))
        not_robbing = models.OrderStatusLogs.objects.aggregate(all_num=Sum('not_robbing'))
        not_pickup = models.OrderStatusLogs.objects.aggregate(all_num=Sum('not_pickup'))
        picking_up = models.OrderStatusLogs.objects.aggregate(all_num=Sum('picking_up'))
        dispatching = models.OrderStatusLogs.objects.aggregate(all_num=Sum('dispatching'))
        pending = models.OrderStatusLogs.objects.aggregate(all_num=Sum('pending'))
        num_dict = {
            'unpaid': unpaid['all_num'],
            'not_robbing': not_robbing['all_num'],
            'not_pickup': not_pickup['all_num'],
            'picking_up': picking_up['all_num'],
            'dispatching': dispatching['all_num'],
            'pending': pending['all_num'],
        }
    else:
        try:
            all_num = models.OrderStatusLogs.objects.get(region_id=request.operator_region)
            num_dict = {
                'unpaid': all_num.unpaid,
                'not_robbing': all_num.not_robbing,
                'not_pickup': all_num.not_pickup,
                'picking_up': all_num.picking_up,
                'dispatching': all_num.dispatching,
                'pending': all_num.pending,
            }
        except Exception:
            num_dict = {
                'unpaid': 0,
                'not_robbing': 0,
                'not_pickup': 0,
                'picking_up': 0,
                'dispatching': 0,
                'pending': 0,
            }
    return render(request, 'Trade/order_list.html',
                  {'data': data_list, 'search_data': search_data, 'get_page': get_page, 'page_total': str(page_total),
                   'num': num_dict})


def order_detail(requst):
    get_order_id = requst.GET.get('order_id')
    order_obj = models.Orders.objects.get(order_id=get_order_id)
    user_obj = models.User.objects.get(user_id=order_obj.user_id)
    sub_obj = models.SubOrders.objects.filter(order_id=get_order_id).all()
    shop_obj = []
    for i in sub_obj:
        shop_obj.append(i.sub_order_id)
    shop_list = []
    shop_remarks_list = []
    for i in shop_obj:
        shop_obj = models.SubOrders.objects.get(sub_order_id=i)
        goods_obj = models.OrderGoods.objects.filter(sub_order_id=i).all()
        goods_list = []
        for j in goods_obj:
            goods_dict = {
                'order_status': shop_obj.order_status,
                'goods_name': j.goods_name,
                'specification_values': j.specification_values,  # 规格搭配
                'attribute_values': j.attribute_values,  # 规格属性
                'unit_price': j.unit_price,  # 单价
                'goods_amount': j.goods_amount,  # 数量
            }
            goods_list.append(goods_dict)
        shop_dict = {
            shop_obj.shop_name: goods_list,
        }
        shop_remarks_dict = {
            shop_obj.shop_name: shop_obj.shop_remarks,
        }
        shop_remarks_list.append(shop_remarks_dict)
        shop_list.append(shop_dict)
    data = {
        'order_id': get_order_id,
        'order_status': order_obj.order_status,  # 配送状态（订单状态）
        'distributor_name': order_obj.distributor_name,
        'distributor_phone_number': order_obj.distributor_phone_number,
        'create_time': order_obj.create_time,
        'pay_time': order_obj.pay_time,
        'complete_time': order_obj.complete_time,
        'total_price': order_obj.total_price,
        'pay_mode': order_obj.pay_mode,  # 支付方式（支付情况）
        'pay_amount': order_obj.pay_amount,  # 支付金额
        'user_name': order_obj.user_name,
        'user_phone_number': order_obj.user_phone_number,  # 接单电话
        'user_address': order_obj.user_address,
        'registe_phone': user_obj.phone_number,  # 用户注册电话
        'distribution_mode': order_obj.distribution_mode,  # 配送方式
        'distribution_remarks': order_obj.distribution_remarks,  # 配送员评价
        'shop_info': shop_list,
        'shop_remarks': shop_remarks_list,
    }
    print(order_obj.pay_mode)
    return render(requst, 'Trade/order_detail.html', {'data': data})
