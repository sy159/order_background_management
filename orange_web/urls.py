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
from django.urls import path
from django.views.decorators.cache import cache_page

from orange_manage import views
from orange_manage.basic_info import views as basic_info
from orange_manage.deliver import views as deliver
from orange_manage.promotion_market import views as promotion_market
from orange_manage.shops import views as merchants
from orange_manage.system_setting import views as system_setting
from orange_manage.trade import views as trade
from orange_manage.users import views as users

urlpatterns = [
    path('', views.home),
    path('admin/', views.home),
    path('admin/login', cache_page(60 * 60 * 24 * 30)(views.login)),  # 登陆
    path('admin/logout', views.logout),  # 注销
    path('admin/bind_account', views.bind_account),  # 两步验证,绑定用户
    path('admin/index/', views.index),  # 主页面
    path('admin/account_unique/', views.account_unique),  # 账号唯一性
    path('admin/image_upload/', views.image_upload),  # 上传图片
    path('admin/kindeditor/', views.kindeditor),  # 在线编辑器
    path('admin/upload_img/', views.upload_img),  # 在线编辑器

    # 商户管理
    path('admin/shop_list/', merchants.shop_list),  # 商户列表
    path('admin/shop_edit/', merchants.shop_edit),  # 商户编辑
    path('admin/store_form/', merchants.store_form),  # 待审核表单
    path('admin/status_form/', merchants.status_form),  # 审核成功表单
    path('admin/fail_form/', merchants.fail_form),  # 审核表单
    path('admin/shop_delete/', merchants.shop_delete),  # 删除商户
    path('admin/wait_store/', merchants.wait_store),  # 待审核
    path('admin/wait_store2/', merchants.wait_store2),  # 审核成功
    path('admin/wait_store3/', merchants.wait_store3),  # 审核失败
    path('admin/category_list/', merchants.category_list),  # 商户分类
    path('admin/add_originalform/', merchants.add_originalform),  # 添加商户分类
    path('admin/edit_originalform/', merchants.edit_originalform),  # 主分类操作
    path('admin/check_childlist/', merchants.check_childlist),  # 查看子分类列表
    path('admin/add_childform/', merchants.add_childform),  # 添加子分类
    path('admin/edit_childform/', merchants.edit_childform),  # 编辑子分类
    path('admin/region_info/', merchants.region_info),  # 省市区信息
    path('admin/circle_list/', merchants.circle_list),  # 商圈列表
    path('admin/add_circle/', merchants.add_circle),  # 添加商圈
    path('admin/edit_circle/', merchants.edit_circle),  # 编辑商圈
    path('admin/store_list/', merchants.store_list),  # 店铺列表
    path('admin/wait_goods/', merchants.wait_goods),  # 待审核商品列表
    path('admin/nopass_goods/', merchants.nopass_goods),  # 审核失败商品列表
    path('admin/goods_details/', merchants.goods_details),  # 商品详情

    # 基本信息相关
    path('admin/account_list/', basic_info.account_list),  # 管理员列表
    path('admin/edit_accountinfo/', basic_info.edit_accountinfo),  # 编辑账号信息
    path('admin/add_account/', basic_info.add_account),  # 添加管理员
    path('admin/permissions/', basic_info.permissions),  # 权限api
    path('admin/edit_authorityform/', basic_info.edit_authorityform),  # 编辑管理员权限弹框
    path('admin/set_authority/', basic_info.set_authority),  # 设置管理员权限弹框
    path('admin/edit_personinfo/', basic_info.edit_personinfo),  # 编辑个人信息
    path('admin/clear_key/', basic_info.clear_key),  # 清除key
    path('admin/choose_address', basic_info.choose_address),  # 选所在地址
    path('admin/region_list', basic_info.region_list),  # 运营区域列表
    path('admin/add_region/', basic_info.add_region),  # 添加运营区域
    path('admin/exist_region/', basic_info.exist_region),  # 存在运营区域列表
    path('admin/edit_region/', basic_info.edit_region),  # 编辑运营区域
    path('admin/campus_list/', basic_info.campus_list),  # 校区列表
    path('admin/add_campusinfo/', basic_info.add_campusinfo),  # 添加校区
    path('admin/edit_campusinfo/', basic_info.edit_campusinfo),  # 编辑校区信息
    path('admin/address_list/', basic_info.address_list),  # 添加详细地址库
    path('admin/add_address/', basic_info.add_address),  # 添加地址
    path('admin/edit_address/', basic_info.edit_address),  # 编辑地址信息

    # 系统设置
    path('admin/adver_management/', system_setting.adver_management),  # 广告管理
    path('admin/adver_list/', system_setting.adver_list),  # 广告列表
    path('admin/adver_add/', system_setting.adver_add),  # 添加广告
    path('admin/choice_stores/', system_setting.choice_stores),  # 选择商店的弹框
    path('admin/choose_goods/', system_setting.choose_goods),  # 选择商品的弹框
    path('admin/choose_shop_category', system_setting.choose_shop_category),  # 选择商品的弹框
    path('admin/adver_edit/', system_setting.adver_edit),  # 编辑广告信息
    path('admin/withdraw_list/', system_setting.withdraw_list),  # 提款列表
    path('admin/modify_status/', system_setting.modify_status),  # 修改支付状态

    path('admin/system_news/', system_setting.system_news_index),  # 平台推文
    path('admin/add_news_category', system_setting.add_news_category),  # 添加推文分类
    path('admin/system_news_list', system_setting.system_news_list),  # 平台推文列表
    path('admin/del_news', system_setting.del_system_news),  # 删除品台推文
    path('admin/edit_news/', system_setting.edit_system_news),  # 添加平台推文
    path('admin/getnews', system_setting.get_system_news),  # 获取推文

    # 用户管理
    path('admin/user_list/', users.user_list),  # 用户列表
    path('admin/user_edit/', users.user_edit),  # 编辑用户

    # 交易管理
    path('admin/order_list/', trade.order_list),  # 订单列表
    path('admin/order_detail/', trade.order_detail),  # 查看订单详情弹框

    # 推广营销
    path('admin/recommend_list/', promotion_market.recommend_list),  # 推荐列表
    path('admin/store_add/', promotion_market.store_add),  # 添加推荐店铺弹窗
    path('admin/store_edit/', promotion_market.store_edit),  # 编辑店铺弹窗

    # 配送管理
    path('admin/marki_manage/', deliver.marki_manage),  # 配送管理
    path('admin/user_add/', deliver.user_add),  # 添加管理员
    path('admin/campus_api/', deliver.campus_api),  # 获取对应的校区信息
    path('admin/deliver_edit/', deliver.deliver_edit),  # 编辑配送员信息
    path('admin/delivery_record/', deliver.delivery_record),  # 查看配送员的配送记录
    path('admin/deliver_list/', deliver.deliver_list),  # 分配配送员列表
    path('admin/marki_list/', deliver.marki_list),  # 调度
    path('admin/marki_api/', deliver.marki_api),  # 未接点单api
    path('admin/order_api/', deliver.order_api),  # 在线配送员api
    path('admin/dispatching_console/', deliver.dispatching_console),  # 调度控制台




]
