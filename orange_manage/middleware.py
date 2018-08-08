from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponseRedirect
from orange_manage import models


class Login_session(MiddlewareMixin):
    def process_request(self, request):
        white_list = ['/admin/login/', ]  # 能够直接访问的url
        if request.path not in white_list:
            if 'judge' not in request.session:
                return HttpResponseRedirect('/admin/login/')
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
        request.shop_image = '/static/shop_image/'
        request.user_image = '/static/user_image/'
        request.banner_images = '/static/banner_images/'
        request.app_menu_images = '/static/app_menu_images/'
        request.recommend_shops_images = '/static/recommend_shops_images/'
