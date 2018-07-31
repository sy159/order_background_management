from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,HttpResponseRedirect

class Login_session(MiddlewareMixin):
    def process_request(self, request):
        white_list = ['/admin/login/',]  # 能够直接访问的url
        if request.path not in white_list:
            if 'judge' not in request.session:
                return HttpResponseRedirect('/admin/login/')
            else:
                pass
