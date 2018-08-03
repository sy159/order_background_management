from django.shortcuts import render, HttpResponse
from orange_manage import models


def user_list(request):
    if request.method=='GET':
        get_keyword = request.GET.get('keyword','')
        get_searchtype = request.GET.get('searchtype')
        get_begin_time = request.GET.get('begin_time','')
        get_end_time = request.GET.get('end_time','')
        get_status = request.GET.get('status','2')
        search_data={
            'keyword':get_keyword,
            'searchtype':get_searchtype,
            'begin_time':get_begin_time,
            'end_time':get_end_time,
            'status':get_status,
        }
        get_pagesize=15
        get_page=request.GET.get('p','1')
        start_nun = int(get_pagesize) * (int(get_page) - 1)  # 起始数据位置
        end_num = start_nun + int(get_pagesize)  # 终止数据位置
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        operator_region = obj.open_admin_region
        if operator_region:
            operator_campus_obj = models.RegionCampus.objects.filter(region_id=operator_region).all()
        else:
            operator_campus_obj=models.RegionCampus.objects.all()
        campus_list=[]
        for i in operator_campus_obj:
            campus_list.append(i.campus_id)
        if len(get_keyword):
            if get_searchtype=='user_id':
                all_obj = models.User.objects.filter(campus_id__in=campus_list,user_id=get_keyword)
            elif get_searchtype=='nickname':
                all_obj = models.User.objects.filter(campus_id__in=campus_list,nickname__contains=get_keyword)
            elif get_searchtype=='phone_number':
                all_obj = models.User.objects.filter(campus_id__in=campus_list, phone_number__contains=get_keyword)
        else:
            all_obj=models.User.objects.filter(campus_id__in=campus_list)
        if get_status!='2':all_obj=all_obj.filter(status=get_status)
        if len(get_begin_time) and len(get_end_time):
            all_obj=all_obj.filter(register_time__gte=get_begin_time)
            all_obj=all_obj.filter(register_time__lte=get_end_time)
        if len(all_obj) % int(get_pagesize):
            page_total = len(all_obj) // int(get_pagesize) + 1
        else:
            page_total = len(all_obj) // int(get_pagesize)
        data_list = []
        for i in all_obj[start_nun:end_num]:
            data_dict = {
                'user_id': i.user_id,
                'nickname': i.nickname,
                'username': i.username,
                'phone_number': i.phone_number,
                'last_ip': i.last_ip,
                'last_login': i.last_login,
                'status': i.status,
                'balance': i.balance,
                'integral': i.integral,
            }
            data_list.append(data_dict)
        return render(request,'User/index.html',{'data':data_list,'get_page':get_page,'page_total':str(page_total),'search_data':search_data})