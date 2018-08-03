from django.shortcuts import render, HttpResponse
from orange_manage import models


def adver_management(request):
    return render(request,'Adver/adver_management.html')


def adver_list(request):
    if request.method == 'GET':
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        operator_region = obj.open_admin_region
        get_id = request.GET.get('id')
        if get_id == '1':
            if operator_region == 0:
                all_obj = models.Banner.objects.all()
            else:
                all_obj = models.Banner.objects.filter(region_id=operator_region).all()
            data_list = []
            for i in all_obj.order_by('-priority'):
                url_type = i.url.split("=")[1].split("#")[0]
                url_id=i.url.split("#")[1]
                if url_type == 'shop':
                    shop_obj = models.Shop.objects.filter(shop_id=url_id).first()
                    url_name = '店铺:'+shop_obj.shop_name
                else:
                    goods_obj = models.Goods.objects.filter(goods_id=url_id).first()
                    shop_obj = models.Shop.objects.filter(shop_id=goods_obj.shop_id).first()
                    url_name = '店铺:'+shop_obj.shop_name+' 商品:'+goods_obj.goods_name
                data_dict = {
                    'id': i.id,
                    'region_id': i.region_id,
                    'title': i.title,
                    'img': 'http://college.cqgynet.com/static/banner_images/'+i.img,
                    'url': url_name,
                    'state': i.state,
                    'start': i.start,
                    'end': i.end,
                    'has_prescription': i.has_prescription,
                }
                data_list.append(data_dict)
            return render(request, 'Adver/adver_list.html', {'data': data_list,'parent_title':'App首页轮播图','parent_id':get_id})
        elif get_id == '2':
            if operator_region == 0:
                all_obj = models.AppMenu.objects.all()
            else:
                all_obj = models.AppMenu.objects.filter(region_id=operator_region).all()
            data_list = []
            for i in all_obj.order_by('-priority'):
                url_type = i.url.split("=")[1].split("#")[0]
                url_id = i.url.split("#")[1]
                if url_type == 'shop':
                    shop_obj = models.Shop.objects.filter(shop_id=url_id).first()
                    url_name = '店铺:'+shop_obj.shop_name
                else:
                    goods_obj = models.Goods.objects.filter(goods_id=url_id).first()
                    shop_obj = models.Shop.objects.filter(shop_id=goods_obj.shop_id).first()
                    url_name = '店铺:'+shop_obj.shop_name+' 商品:'+goods_obj.goods_name
                data_dict = {
                    'id': i.id,
                    'region_id': i.region_id,
                    'title': i.title,
                    'img': 'http://college.cqgynet.com/static/appmenu_images/'+i.img,
                    'url': url_name,
                    'state': i.state,
                }
                data_list.append(data_dict)
            return render(request, 'Adver/adver_list.html', {'data': data_list,'parent_title':'App首页菜单','parent_id':get_id})
    elif request.method == 'DELETE':
        get_parent_id = request.GET.get('parent_id')
        get_id = request.GET.get('adver_id')
        if get_parent_id == '1':
            models.Banner.objects.filter(id=get_id).delete()
        elif get_parent_id == '2':
            models.AppMenu.objects.filter(id=get_id).delete()
        return HttpResponse(1)


def adver_add(request):
    if request.method=='GET':
        get_id = request.GET.get('parent_id')

        return render(request, 'Adver/adver_add.html',{'parent_id':get_id})
    elif request.method=='POST':
        get_id = request.GET.get('parent_id')
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        operator_region = obj.open_admin_region
        get_title=request.POST.get("adver_name")
        get_status=request.POST.get("status")
        get_img=request.POST.get("img")
        get_priority=request.POST.get("sort")
        get_url=request.POST.get("get_url")#获取格式为shop_id=9或者goods_id=9
        if 'shop' in get_url:
            get_url='?a=shop#'+get_url.split('=')[1]
        else:
            get_url='?a=goods#'+get_url.split('=')[1]

        if get_id=='1':
            models.Banner.objects.create(title=get_title,img=get_img,url=get_url,priority=get_priority,state=get_status,region_id=operator_region)
        elif get_id=='2':
            models.AppMenu.objects.create(title=get_title,img=get_img,url=get_url,priority=get_priority,state=get_status,region_id=operator_region)
        return HttpResponse(1)


def stores(request):
    get_flag = request.GET.get('flag')
    get_parent_id = request.GET.get('parent_id')
    get_adver_id = request.GET.get('adver_id')
    get_operator = request.session.get('user')
    obj = models.Admin.objects.filter(account=get_operator).first()
    operator_region = obj.open_admin_region
    if request.method=='GET':
        get_page=request.GET.get('p','1')
        get_pagesize=5
        get_search_content=request.GET.get('keyword')
        if get_search_content:
            if operator_region==0:
                all_obj=models.Shop.objects.filter(auth=2,status=1,shop_name__contains=get_search_content).all()#审核通过，状态开启
            else:
                all_obj=models.Shop.objects.filter(auth=2,status=1,region_id=operator_region,shop_name__contains=get_search_content).all()#审核通过，状态开启
        else:
            if operator_region==0:
                all_obj=models.Shop.objects.filter(auth=2,status=1).all()#审核通过，状态开启
            else:
                all_obj=models.Shop.objects.filter(auth=2,status=1,region_id=operator_region).all()#审核通过，状态开启
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'shop_id': i.shop_id,
                'shop_name': i.shop_name,
            }
            data_list.append(data_dict)
        return render(request, 'Adver/stores.html',{'data':data_list,'get_page':get_page,'page_total':str(page_total),'flag':get_flag,'parent_id':get_parent_id,'adver_id':get_adver_id})


def goods(request):
    get_shop_id=request.GET.get('shop_id')
    get_parent_id=request.GET.get('parent_id')
    get_adver_id=request.GET.get('adver_id')
    get_stores =request.GET.get('stores')
    get_flag = request.GET.get('flag')
    if request.method=='GET':
        get_pagesize=5
        get_page=request.GET.get('p','1')
        get_search_content = request.GET.get('keyword')
        if get_search_content:
            all_obj = models.Goods.objects.filter(shop_id=get_shop_id,goods_name__contains=get_search_content).all()
        else:
            all_obj = models.Goods.objects.filter(shop_id=get_shop_id).all()
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'goods_id': i.goods_id,
                'goods_name': i.goods_name,
            }
            data_list.append(data_dict)
        return render(request, 'Adver/goods.html',{'data':data_list,'get_page':get_page,'page_total':str(page_total),'stores':get_stores,'shop_id':get_shop_id,'flag':get_flag,'parent_id':get_parent_id,'adver_id':get_adver_id})


def adver_edit(request):
    if request.method=='GET':
        get_parent_id = request.GET.get('parent_id')
        get_adver_id = request.GET.get('adver_id')
        if get_parent_id=='1':#首页轮播
            obj=models.Banner.objects.filter(id=get_adver_id).first()
            img='http://college.cqgynet.com/static/banner_images/'+obj.img
        elif get_parent_id=='2':#菜单
            obj=models.AppMenu.objects.filter(id=get_adver_id).first()
            img = 'http://college.cqgynet.com/static/appmenu_images/'+ obj.img
        data_dict={
            'adver_id':get_adver_id,
            'title':obj.title,
            'img':img,
            'priority':obj.priority,
            'state':obj.state
        }
        return render(request, 'Adver/adver_edit.html',{'data':data_dict,'parent_id':get_parent_id})
    elif request.method=='POST':
        get_parent_id = request.POST.get('parent_id')
        get_shop_id = request.POST.get('adver_id')
        if get_parent_id=='1':#轮播图
            obj=models.Banner.objects.filter(id=get_shop_id).first()
        elif get_parent_id=='2':#菜单栏
            obj = models.AppMenu.objects.filter(id=get_shop_id).first()
        get_title = request.POST.get('name')
        get_status = request.POST.get('status')
        get_img = request.POST.get('img')
        get_priority = request.POST.get('sort')
        get_url = request.POST.get('get_url')  # 获取格式为shop_id=9或者goods_id=9
        if not len(get_title):get_title=obj.title
        if not len(get_status):get_status=obj.state
        if not len(get_img):get_img=obj.img
        if not len(get_priority):get_priority=obj.priority
        if not len(get_url):get_url=obj.url
        if 'shop' in get_url:
            get_url = '?a=shop#' + get_url.split('=')[1]
        else:
            get_url = '?a=goods#' + get_url.split('=')[1]
        if get_parent_id=='1':#轮播图
            models.Banner.objects.filter(id=get_shop_id).update(title=get_title,img=get_img,url=get_url,state=get_status,priority=get_priority)
        elif get_parent_id=='2':#菜单栏
            models.AppMenu.objects.filter(id=get_shop_id).update(title=get_title,img=get_img,url=get_url,state=get_status,priority=get_priority)
        return HttpResponse(1)