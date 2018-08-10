from orange_manage import models

def region_list():
    all_obj=models.RegionCampus.objects.all()
    data_list = []
    for i in all_obj:
        if str(i.region_id) not in str(data_list):
            obj=models.Region.objects.get(region_id=i.region_id)
            region_id_list=[]
            region_id_list.append(i.region_id)
            region_id_list.append(obj.region_name)
            data_list.append(region_id_list)
    return data_list


def campus_list(region):
    all_obj=models.RegionCampus.objects.filter(region_id=region)
    data_list=[]
    for i in all_obj:
        obj=models.Campus.objects.get(campus_id=i.campus_id)
        data=[]
        data.append(i.campus_id)
        data.append(obj.campus)
        data_list.append(data)
    return data_list