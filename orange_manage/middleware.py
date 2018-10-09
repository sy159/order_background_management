from django.shortcuts import HttpResponseRedirect
# 兼容新旧版本的django
from orange_manage import models

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class LoginSession(MiddlewareMixin):
    def process_request(self, request):
        white_list = ['/admin/login']  # 能够直接访问的url
        if request.path not in white_list:
            if 'judge' not in request.session:
                return HttpResponseRedirect('/admin/login')
            else:
                pass


class GlobalInfo(MiddlewareMixin):
    def process_request(self, request):
        get_operator = request.session.get('user')
        obj = models.Admin.objects.filter(account=get_operator).first()
        if obj:
            request.operator_region = obj.open_admin_region
            request.operator_level = obj.level
            request.operator_menus = obj.menus
            request.operator_name = get_operator
            request.operator_id = obj.id
            request.operator_obj = obj
        request.FTP_HOST = "http://ftp.college.cqgynet.com"  # 图片访问域名
        request.goods_image = '/static/goods_images/'
        request.shop_image = '/static/shop_images/'
        request.user_image = '/static/user_images/'
        request.banner_images = '/static/banner_images/'
        request.app_menu_images = '/static/app_menu_images/'
        request.recommend_shops_images = '/static/recommend_shops_images/'
        request.distributor_image = '/static/distributor_images/'
        request.coupon_images = '/static/coupon_images/'
