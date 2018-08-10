from django.shortcuts import render, redirect, HttpResponse
from orange_manage import models
from django.http import JsonResponse
from orange_manage.utils.campus_info import campus_list, region_list
from django.utils import timezone


def marki_manage(request):
    if request.method == 'GET':
        get_page = request.GET.get('p', '1')
        get_pagesize = 15
        get_keyword = request.GET.get('keyword')
        get_searchtype = request.GET.get('searchtype')
        data_status = {
            'keyword': get_keyword,
            'searchtype': get_searchtype,
        }
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        get_region = request.operator_region
        if get_region == 0:
            all_obj = models.Distributor.objects.all()
        else:
            all_obj = models.Distributor.objects.filter(region_id=get_region)
        if get_keyword:
            if get_searchtype == 'distributor_id':
                all_obj = all_obj.filter(distributor_id=get_keyword)
            elif get_searchtype == 'name':
                all_obj = all_obj.filter(name__contains=get_keyword)
            elif get_searchtype == 'phone_number':
                all_obj = all_obj.filter(phone_number__contains=get_keyword)
        page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
            get_pagesize)
        data_list = []
        all_obj.query.group_by = ['region_id']
        for i in all_obj.order_by('-priority')[start_nun:end_num]:
            obj = models.Campus.objects.get(campus_id=i.campus_id)
            data_dict = {
                'distributor_id': i.distributor_id,
                'name': i.name,
                'gender': i.gender,
                'phone_number': i.phone_number,
                'campus_id': i.campus_id,
                'campus_name': obj.campus,
                'priority': i.priority,
                'status': i.status,
                'is_part_time': i.is_part_time,
            }
            data_list.append(data_dict)
        return render(request, 'Deliver/user.html',
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total),
                       'data_status': data_status})
    if request.method == 'DELETE':
        get_id = request.GET.get('user_id')
        models.Distributor.objects.get(distributor_id=get_id).delete()
        return HttpResponse(1)


def user_add(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'username': request.POST.get('phone_number'),
            'phone_number': request.POST.get('phone_number'),
            'gender': request.POST.get('gender'),
            'id_number': request.POST.get('id_number'),
            'region_id': request.POST.get('region', request.operator_region),
            'campus_id': request.POST.get('campus'),
            'student_number': request.POST.get('student_number'),
            'profile_image': request.POST.get('img'),
            'register_time': timezone.now(),
            'priority': request.POST.get('priority'),
            'status': request.POST.get('status'),
            'is_part_time': 0,
        }
        models.Distributor.objects.create(**data)
        return HttpResponse(1)
    if request.operator_region == 0:
        data_list = region_list()
        return render(request, 'Deliver/user_add.html', {'data': data_list})
    data_list = campus_list(request.operator_region)
    return render(request, 'Deliver/user_add.html', {'data': data_list, 's': 1})


def deliver_edit(request):
    if request.method == 'GET':
        get_id = request.GET.get('user_id')
        obj = models.Distributor.objects.get(distributor_id=get_id)
        if request.operator_region == 0:
            s = '0'
            data_list = region_list()
        else:
            s = '1'
            data_list = campus_list(obj.region_id)
        data = {
            'deliver_id': get_id,
            'name': obj.name,
            'username': obj.username,
            'phone_number': obj.phone_number,
            'gender': obj.gender,
            'id_number': obj.id_number,
            'region_id': obj.region_id,
            'campus_id': obj.campus_id,
            'student_number': obj.student_number,
            'profile_image': request.FTP_HOST + request.distributor_image + obj.profile_image,
            'priority': obj.priority,
            'status': obj.status,
            'is_part_time': obj.is_part_time,
        }
        return render(request, 'Deliver/user_edit.html', {'data': data, 's': s, 'data_list': data_list})
    elif request.method == 'POST':
        data = {
            'distributor_id': request.POST.get('deliver_id'),
            'name': request.POST.get('name'),
            'username': request.POST.get('phone_number'),
            'phone_number': request.POST.get('phone_number'),
            'gender': request.POST.get('gender'),
            'id_number': request.POST.get('id_number'),
            'region_id': request.POST.get('region', request.operator_region),
            'campus_id': request.POST.get('campus'),
            'student_number': request.POST.get('student_number'),
            'priority': request.POST.get('priority'),
            'status': request.POST.get('status'),
            'is_part_time': request.POST.get('is_part_time'),
        }
        if request.POST.get('img'): data['profile_image'] = request.POST.get('img')
        models.Distributor.objects.filter(distributor_id=request.POST.get('deliver_id')).update(**data)
        return HttpResponse(1)


def campus_api(request):
    get_region = request.GET.get('region_id')
    data = campus_list(get_region)
    return JsonResponse(data, safe=False)


def delivery_record(request):
    get_page = request.GET.get('p', '1')
    get_pagesize = 15
    start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
    end_num = start_nun + int(get_pagesize)  # 终止数据位置
    get_distributor_id = request.GET.get('distributor_id')
    all_obj = models.Orders.objects.filter(distributor_id=get_distributor_id)
    data_list = []
    distributor_obj = models.Distributor.objects.get(distributor_id=get_distributor_id)
    begin_time = request.GET.get('begin_time')
    end_time = request.GET.get('end_time')
    status_data = {
        'begin_time': begin_time,
        'end_time': end_time,
    }
    if begin_time and end_time:
        all_obj = all_obj.filter(complete_time__gte=begin_time)
        all_obj = all_obj.filter(complete_time__lte=end_time)
    page_total = len(all_obj) // int(get_pagesize) + 1 if len(all_obj) % int(get_pagesize) else len(all_obj) // int(
        get_pagesize)
    for i in all_obj[start_nun:end_num]:
        try:
            cost_time = i.complete_time - i.distribution_start_time
        except Exception:
            cost_time = ''
        data_dict = {
            'order_id': i.order_id,
            'user_name': i.user_name,
            'user_phone_number': i.user_phone_number,
            'user_address': i.user_address,
            'pay_mode': i.pay_mode,
            'total_price': i.total_price,
            'distribution_fee': i.distribution_fee,
            'distribution_start_time': i.distribution_start_time,
            'complete_time': i.complete_time,
            'cost_time': cost_time,
            'distribution_status': i.distribution_status,
        }
        data_list.append(data_dict)
    return render(request, 'Deliver/Delivery_record.html',
                  {'data': data_list, 'distributor_name': distributor_obj.name, 'distributor_id': get_distributor_id,
                   'status_data': status_data, 'get_page': get_page, 'page_total': str(page_total)})
