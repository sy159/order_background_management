from orange_manage import models


def region_data():
    province_id_list = []  # 存放省id
    province_data = []  # 存放省数据
    city_id_list = []  # 存放市id
    city_data = {}  # 存放市数据
    area_id_list = []  # 存放区县id
    area_data = {}  # 存放区县数据
    region_data = {}  # 存放运营区域数据
    data = []  # 返回的所有数据
    all_obj = models.Region.objects.all()
    for i in all_obj:
        if i.province_id not in province_id_list:
            province_id_list.append(i.province_id)
    for i in province_id_list:
        province_obj = models.AddresLibrary.objects.filter(id=i).first()
        province_dict = {'province_id': i, 'province_name': province_obj.site_name}  # 所有的省
        province_data.append(province_dict)
    data.append(province_data)
    for i in province_id_list:
        city_all_obj = models.Region.objects.filter(province_id=i).all()
        city_list = []
        for j in city_all_obj:
            city_obj = models.AddresLibrary.objects.filter(id=j.city_id).first()
            city_dict = {'city_id': j.city_id, 'city_name': city_obj.site_name}  # 所有的市
            if city_dict not in city_list:
                city_list.append(city_dict)
            if j.city_id not in city_id_list:
                city_id_list.append(j.city_id)
        city_data[i] = city_list
    data.append(city_data)
    for i in city_id_list:
        area_all_obj = models.Region.objects.filter(city_id=i).all()
        area_list = []
        for j in area_all_obj:
            area_obj = models.AddresLibrary.objects.filter(id=j.area_id).first()
            area_name = area_obj.site_name
            area_dict = {'area_id': j.area_id, 'area_name': area_name}  # 所有的区/县
            if area_dict not in area_list:
                area_list.append(area_dict)
            if j.area_id not in area_id_list:
                area_id_list.append(j.area_id)
        area_data[i] = area_list
    data.append(area_data)
    for i in area_id_list:
        region_all_obj = models.Region.objects.filter(area_id=i).all()
        region_list = []
        for j in region_all_obj:
            region_dict = {'region_id': j.region_id, 'region_name': j.region_name}  # 所有的管理区域
            if region_dict not in region_list:
                region_list.append(region_dict)
        region_data[i] = region_list
    data.append(region_data)
    return data
