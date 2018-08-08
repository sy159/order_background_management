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
                      {'data': data_list, 'get_page': get_page, 'page_total': str(page_total)})
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
        print(data_dict)
        models.RecommendShops.objects.filter(id=get_id).update(**data_dict)
        return HttpResponse(1)
