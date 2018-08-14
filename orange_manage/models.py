# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddresLibrary(models.Model):
    superior_id = models.IntegerField(blank=True, null=True)
    site_name = models.CharField(max_length=255)
    character = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'addres_library'


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    campus_id = models.IntegerField()
    parent_id = models.IntegerField()
    value = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    have_subordinate = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'address'


class Admin(models.Model):
    account = models.CharField(max_length=20)
    pwd = models.CharField(max_length=255)
    realname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    qq = models.CharField(max_length=20)
    last_ip = models.CharField(max_length=20)
    last_time = models.DateTimeField()
    login_count = models.IntegerField()
    status = models.IntegerField()
    level = models.PositiveIntegerField()
    menus = models.TextField()
    openid = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=50)
    permission_group = models.CharField(max_length=200, blank=True, null=True)
    sort_menus = models.CharField(max_length=1000)
    open_admin_region = models.IntegerField()
    authority_group_id = models.IntegerField(blank=True, null=True)
    admin_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class AppMenu(models.Model):
    region_id = models.IntegerField()
    title = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    state = models.IntegerField()
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_menu'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Banner(models.Model):
    region_id = models.IntegerField()
    title = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    state = models.IntegerField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField()
    has_prescription = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banner'


class Campus(models.Model):
    campus_id = models.AutoField(primary_key=True)
    campus = models.CharField(max_length=255)
    university_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campus'


class CashApplications(models.Model):
    identity = models.IntegerField()
    account_id = models.IntegerField()
    cash_account_type = models.IntegerField()
    cash_account = models.CharField(max_length=255)
    account_holder = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()
    operator_id = models.IntegerField(blank=True, null=True)
    operator_name = models.CharField(max_length=255, blank=True, null=True)
    operator_phone = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    payment_time = models.DateTimeField(blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    account_phone = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'cash_applications'


class Circle(models.Model):
    circle_id = models.AutoField(primary_key=True)
    circle_name = models.CharField(max_length=255)
    region_id = models.IntegerField()
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'circle'


class CircleShop(models.Model):
    record_id = models.AutoField(primary_key=True)
    circle_id = models.IntegerField()
    shop_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'circle_shop'


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255)
    province_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'city'


class CommentImage(models.Model):
    record_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    image = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'comment_image'


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    county = models.CharField(max_length=255)
    city_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'county'


class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    shop_id = models.IntegerField()
    coupon_type = models.IntegerField()
    use_condition = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    validity_period = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    amount = models.IntegerField()
    total_amount = models.IntegerField()
    limit_quantity = models.IntegerField()
    status = models.IntegerField()
    superposable = models.IntegerField()
    is_specific = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coupon'


class CouponGoods(models.Model):
    record_id = models.AutoField(primary_key=True)
    coupon_id = models.IntegerField()
    type = models.IntegerField()
    target_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coupon_goods'


class Distributor(models.Model):
    distributor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField()
    phone_number = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    campus_id = models.IntegerField()
    student_number = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    register_time = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_part_time = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    alipay_account = models.CharField(max_length=255, blank=True, null=True)
    account_holder = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    online = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'distributor'


class DistributorTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField(blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    distributor_id = models.IntegerField()
    distributor_name = models.CharField(max_length=255)
    amount = models.FloatField()
    time = models.DateTimeField()
    pay_mode = models.IntegerField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    in_or_out = models.IntegerField()
    campus_id = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distributor_transaction'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Goods(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    shop_id = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)
    pack_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    classify_id = models.IntegerField()
    status = models.IntegerField()
    privilege = models.IntegerField()
    platform_classify_id = models.IntegerField(blank=True, null=True)
    purchasing_limitation = models.PositiveIntegerField(blank=True, null=True)
    sales_amount = models.PositiveIntegerField(blank=True, null=True)
    total_sales_amount = models.IntegerField(blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods'


class GoodsAttribute(models.Model):
    record_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    attribute_name = models.CharField(max_length=255)
    attribute_values = models.CharField(max_length=255, blank=True, null=True)
    sub_order_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_attribute'


class GoodsAttributeName(models.Model):
    attribute_name_id = models.AutoField(primary_key=True)
    attribute_name = models.CharField(max_length=255)
    max_selected_num = models.IntegerField()
    goods_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_attribute_name'


class GoodsAttributeValue(models.Model):
    attribute_value_id = models.AutoField(primary_key=True)
    attribute_name_id = models.IntegerField()
    attribute_value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'goods_attribute_value'


class GoodsClassify(models.Model):
    record_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    name = models.CharField(max_length=255)
    shop_id = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    week_time = models.CharField(max_length=255)
    privilege = models.IntegerField()
    is_show = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_classify'


class GoodsComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255)
    time = models.DateTimeField()
    comment_content = models.CharField(max_length=255)
    to_comment_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_comment'


class GoodsImage(models.Model):
    record_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    image = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'goods_image'


class GoodsInfo(models.Model):
    goods_id = models.IntegerField(primary_key=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    product_standard_number = models.CharField(max_length=255, blank=True, null=True)
    producing_area = models.CharField(max_length=255, blank=True, null=True)
    quality_guarantee_period = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_info'


class GoodsSpecName(models.Model):
    spec_name_id = models.AutoField(primary_key=True)
    spec_name = models.CharField(max_length=255)
    goods_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_spec_name'


class GoodsSpecValue(models.Model):
    spec_value_id = models.AutoField(primary_key=True)
    spec_name_id = models.IntegerField()
    spec_value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'goods_spec_value'


class GoodsSpecification(models.Model):
    specification_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    unit = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField()
    sales_amount = models.PositiveIntegerField(blank=True, null=True)
    spec = models.CharField(max_length=1000, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_specification'


class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField()
    field_function_name = models.CharField(db_column='\nfunction_name', max_length=255)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_function_url = models.CharField(db_column='\nfunction_url', max_length=255)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'menu'


class NecessaryGoods(models.Model):
    record_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField()
    goods_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'necessary_goods'


class OrderGoods(models.Model):
    record_id = models.AutoField(primary_key=True)
    sub_order_id = models.CharField(max_length=255)
    goods_id = models.IntegerField()
    specification_id = models.IntegerField(blank=True, null=True)
    goods_name = models.CharField(max_length=255)
    goods_amount = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recovery = models.IntegerField()
    recovery_id = models.IntegerField(blank=True, null=True)
    specification_values = models.CharField(max_length=255, blank=True, null=True)
    attribute_values = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_goods'


class OrderStatusLogs(models.Model):
    id = models.IntegerField(primary_key=True)
    region_id = models.IntegerField()
    unpaid = models.IntegerField()
    not_robbing = models.IntegerField()
    not_pickup = models.IntegerField()
    picking_up = models.IntegerField()
    dispatching = models.IntegerField()
    pending = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_status_logs'


class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=255)
    order_status = models.IntegerField()
    user_id = models.IntegerField()
    distributor_id = models.IntegerField(blank=True, null=True)
    distributor_name = models.CharField(max_length=255, blank=True, null=True)
    distributor_phone_number = models.CharField(max_length=255, blank=True, null=True)
    distributor_comment = models.CharField(max_length=255, blank=True, null=True)
    distributor_service_rating = models.IntegerField(blank=True, null=True)
    distributor_speed_rating = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    pay_time = models.DateTimeField(blank=True, null=True)
    order_get_time = models.DateTimeField(blank=True, null=True)
    goods_get_time = models.DateTimeField(blank=True, null=True)
    distribution_start_time = models.DateTimeField(blank=True, null=True)
    complete_time = models.DateTimeField(blank=True, null=True)
    distribution_mode = models.IntegerField(blank=True, null=True)
    distribution_remarks = models.CharField(max_length=255, blank=True, null=True)
    distribution_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    coupon_id = models.IntegerField(blank=True, null=True)
    coupon_type = models.IntegerField(blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_mode = models.IntegerField(blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unfinished_reason = models.CharField(max_length=255, blank=True, null=True)
    campus_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_phone_number = models.CharField(max_length=255, blank=True, null=True)
    user_address = models.CharField(max_length=255, blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    address_type = models.IntegerField(blank=True, null=True)
    goods_amount = models.IntegerField(blank=True, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    trade_no = models.CharField(max_length=255, blank=True, null=True)
    last_up_time = models.BigIntegerField(blank=True, null=True)
    distribution_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Point(models.Model):
    point_id = models.AutoField(primary_key=True)
    remitter_id = models.IntegerField()
    remitter_nick = models.CharField(max_length=255)
    payee_id = models.IntegerField()
    payee_nick = models.CharField(max_length=255)
    amount = models.IntegerField()
    time = models.DateTimeField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    mode = models.CharField(max_length=1)
    university_id = models.IntegerField()
    campus_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'point'


class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'province'


class RecommendShops(models.Model):
    shop_id = models.IntegerField()
    shop_name = models.CharField(max_length=255)
    priority = models.IntegerField(blank=True, null=True)
    operator_name = models.CharField(max_length=255)
    last_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    img = models.CharField(max_length=255)
    region_id = models.IntegerField()
    operator_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'recommend_shops'


class Recovery(models.Model):
    recovery_id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    collector_id = models.IntegerField(blank=True, null=True)
    box_num = models.IntegerField()
    chopstick_num = models.IntegerField()
    fork_num = models.IntegerField()
    spoon_num = models.IntegerField()
    place_time = models.DateTimeField()
    recovery_time = models.DateTimeField()
    is_finished = models.CharField(max_length=1, blank=True, null=True)
    unfinished_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recovery'


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    province_id = models.IntegerField()
    city_id = models.IntegerField()
    area_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'region'


class RegionCampus(models.Model):
    record_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField()
    campus_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'region_campus'


class RegionConfig(models.Model):
    id = models.IntegerField(primary_key=True)
    region_id = models.IntegerField()
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_config'


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255)
    shop_logo = models.CharField(max_length=255)
    campus_id = models.IntegerField()
    region_id = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    shop_type = models.IntegerField()
    province = models.IntegerField()
    city = models.IntegerField()
    county = models.IntegerField()
    address = models.CharField(max_length=255)
    business_license = models.CharField(max_length=255)
    catering_license = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    manager_id = models.IntegerField()
    default_account = models.IntegerField(blank=True, null=True)
    bank_account_holder = models.CharField(max_length=255, blank=True, null=True)
    bank_account = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    shop_photos = models.CharField(max_length=255, blank=True, null=True)
    packing_commission = models.IntegerField()
    auth = models.IntegerField()
    start_business_time = models.TimeField(blank=True, null=True)
    end_business_time = models.TimeField(blank=True, null=True)
    notice = models.CharField(max_length=255, blank=True, null=True)
    status = models.PositiveIntegerField()
    money = models.DecimalField(max_digits=10, decimal_places=2)
    money_state = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    packing_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop'


class ShopAccount(models.Model):
    record_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=255)
    account_type = models.IntegerField()
    shop_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shop_account'


class ShopAssistant(models.Model):
    shop_assistant_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    is_assistant = models.IntegerField()
    university_id = models.IntegerField(blank=True, null=True)
    campus_id = models.IntegerField(blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    register_time = models.DateTimeField()
    last_login = models.DateTimeField()
    permission = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_assistant'


class ShopAuditLog(models.Model):
    shop_id = models.IntegerField()
    auth = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    operator_id = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_audit_log'


class ShopComment(models.Model):
    record_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField()
    sub_order_id = models.IntegerField()
    shop_rating = models.IntegerField(blank=True, null=True)
    shop_comment = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_comment'


class ShopNoticesLog(models.Model):
    id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    notice = models.CharField(max_length=255, blank=True, null=True)
    create_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_notices_log'


class ShopPhoto(models.Model):
    record_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField()
    photo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_photo'


class ShopSort(models.Model):
    sort_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    sort_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField()
    state = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shop_sort'


class SmsSendLogs(models.Model):
    addressee = models.CharField(max_length=255)
    action_type = models.IntegerField(blank=True, null=True)
    identity_type = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255)
    verify_code = models.CharField(max_length=255, blank=True, null=True)
    valid_till = models.DateTimeField(blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_send_logs'


class SmsTemplate(models.Model):
    template_id = models.IntegerField(blank=True, null=True)
    template_content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_template'


class SubOrders(models.Model):
    sub_order_id = models.CharField(primary_key=True, max_length=255)
    order_status = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    packing_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    coupon_id = models.IntegerField(blank=True, null=True)
    coupon_type = models.IntegerField(blank=True, null=True)
    coupon_value = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField()
    pay_time = models.DateTimeField(blank=True, null=True)
    goods_get_time = models.DateTimeField(blank=True, null=True)
    distribution_start_time = models.DateTimeField(blank=True, null=True)
    distributor_id = models.IntegerField(blank=True, null=True)
    distributor_name = models.CharField(max_length=255, blank=True, null=True)
    shop_id = models.IntegerField()
    shop_name = models.CharField(max_length=255)
    shop_assistant_id = models.IntegerField(blank=True, null=True)
    shop_assistant_name = models.CharField(max_length=255, blank=True, null=True)
    shop_remarks = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_phone_number = models.CharField(max_length=255, blank=True, null=True)
    user_address = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    address_type = models.IntegerField(blank=True, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_orders'


class Test(models.Model):
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test'


class TransactionRecords(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    transaction_no = models.CharField(max_length=255)
    drawee = models.CharField(max_length=255)
    payee = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'transaction_records'


class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'university'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    gender = models.IntegerField()
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    campus_id = models.IntegerField(blank=True, null=True)
    register_time = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_part_time = models.IntegerField(blank=True, null=True)
    spread_code = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    is_verified = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    accumulative_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    payment_password = models.CharField(max_length=255, blank=True, null=True)
    integral = models.PositiveIntegerField()
    last_ip = models.CharField(max_length=20, blank=True, null=True)
    qq = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserAddress(models.Model):
    user_address_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    region_id = models.IntegerField()
    address_type = models.IntegerField()
    campus_id = models.IntegerField()
    interior_component = models.CharField(max_length=255, blank=True, null=True)
    interior_detail = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    other_address = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.IntegerField()
    is_default = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_address'


class UserCoupon(models.Model):
    record_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    coupon_id = models.IntegerField()
    create_time = models.DateTimeField()
    coupon_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    coupon_type = models.IntegerField()
    use_condition = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    use_time = models.DateTimeField(blank=True, null=True)
    superposable = models.IntegerField(blank=True, null=True)
    is_specific = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_coupon'


class UserTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField(blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    amount = models.FloatField()
    time = models.DateTimeField()
    pay_mode = models.IntegerField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    in_or_out = models.IntegerField()
    campus_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_transaction'
