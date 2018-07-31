"""orange_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,re_path
from orange_manage import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/login/', views.login),#登陆
    path('admin/logout/', views.logout),#注销
    path('admin/bind_account/', views.bind_account),#两步验证,绑定用户
    path('admin/index/', views.index),#主页面

#改了东西

    #商户管理
    path('admin/shop_list/', views.shop_list),#商户列表
    path('admin/shop_edit/', views.shop_edit),#商户编辑
    path('admin/store_form/', views.store_form),#待审核表单
    path('admin/status_form/', views.status_form),#审核成功表单
    path('admin/fail_form/', views.fail_form),#审核表单
    path('admin/shop_delete/', views.shop_delete),#删除商户
    path('admin/wait_store/', views.wait_store),#待审核
    path('admin/wait_store2/', views.wait_store2),#审核成功
    path('admin/wait_store3/', views.wait_store3),#审核失败
    path('admin/category_list/', views.category_list),#商户分类
    path('admin/add_originalform/', views.add_originalform),#添加商户分类
    path('admin/edit_originalform/', views.edit_originalform),#主分类操作
    path('admin/check_childlist/', views.check_childlist),#查看子分类列表
    path('admin/add_childform/', views.add_childform),#添加子分类
    path('admin/edit_childform/', views.edit_childform),#编辑子分类
    path('admin/region_info/', views.region_info),#省市区信息
    path('admin/test/', views.test),

    #基本信息相关
    path('admin/account_list/', views.account_list),#管理员列表
    path('admin/edit_accountinfo/', views.edit_accountinfo),#编辑账号信息
    path('admin/authority_group/', views.authority_group),
    path('admin/add_account/', views.add_account),#添加管理员
    path('admin/permissions/', views.permissions),#权限api
    path('admin/account_unique/', views.account_unique),#账号唯一性


]

