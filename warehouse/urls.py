"""warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page


from account.views import *
from depot.views import *


urlpatterns = [
    # 首页
    # path('', cache_page(60 * 60)(TemplateView.as_view(template_name='modern-business/index.html')), name='index'),
    path('', TemplateView.as_view(template_name='modern-business/index.html'), name='index'),
    # 首页
    # path('index/', cache_page(60 * 60)(TemplateView.as_view(template_name='modern-business/index.html')), name='index'),
    path('index/', TemplateView.as_view(template_name='modern-business/index.html'), name='index'),

    #admin页面
    path('admin/', admin.site.urls, name='admin'),

    #后台首页
    path('backend/', include('backend.urls')),

    ###后台功能

    #订单url
    path('', include('order.urls')),

    ##账户操作

    # 登录
    # path('login/', cache_page(60 * 60)(auth_views.login), {'template_name': 'login.html', }, name='login'),
    path('login/', cache_page(60 * 60)(auth_views.login), {'template_name': 'login.html', }, name='login'),
    # 注销
    path('logout/', auth_views.logout_then_login, {'login_url': 'login', }, name='logout'),

    #用户列表查询
    path('account_list/',account_list,name='account_list'),
    # 创建账户
    path('account_create/', account_create, name='account_create'),
    # 管理员重置用户密码
    path('password_set/<int:id>/', password_set, name='password_set'),
    # 删除用户
    path('account_edit/<int:id>/', account_edit, name='account_edit'),
    # 删除用户
    path('account_del/<int:id>/', account_del, name='account_del'),

    #当前用户编辑个人资料
    path('account_profile/<int:id>/', account_profile, name='account_profile'),
    # 当前用户修改密码
    path('password_change/', password_change, name='password_change'),
    # 查看当前用户操作记录
    path('account_operate_record/', account_operate_record, name='account_operate_record'),

    #公司分级查询、修改、删除
    path('level_list/', level_list, name='level_list'),
    path('level_edit/<int:id>/', level_edit, name='level_edit'),
    path('level_del/<int:id>/', level_del, name='level_del'),

    #用户组查询、修改、删除
    path('group_list/', group_list, name='group_list'),
    path('group_edit/<int:id>/', group_edit, name='group_edit'),
    path('group_del/<int:id>/', group_del, name='group_del'),

    #公司查询、修改、删除
    path('company_list/', company_list, name='company_list'),
    path('company_edit/<int:id>/', company_edit, name='company_edit'),
    path('company_del/<int:id>/', company_del, name='company_del'),


    #仓库查询、修改、删除
    path('depot_list/', depot_list, name='depot_list'),
    path('depot_edit/<int:id>/', depot_edit, name='depot_edit'),
    path('depot_del/<int:id>/', depot_del, name='depot_del'),

    #库位查询、修改、删除
    path('unit_list/', unit_list, name='unit_list'),
    path('unit_edit/<int:id>/', unit_edit, name='unit_edit'),
    path('unit_del/<int:id>/', unit_del, name='unit_del'),
    # 库位初始化
    path('unit_init/', unit_init, name='unit_init'),

    #SKU类别查询、修改、删除
    path('skutype_list/', skutype_list, name='skutype_list'),
    path('skutype_edit/<int:id>/', skutype_edit, name='skutype_edit'),
    path('skutype_del/<int:id>/', skutype_del, name='skutype_del'),

    # SKU类别费用查询、修改、删除
    path('skutypefee_list/', skutypefee_list, name='skutypefee_list'),
    path('skutypefee_edit/<int:id>/', skutypefee_edit, name='skutypefee_edit'),
    path('skutypefee_del/<int:id>/', skutypefee_del, name='skutypefee_del'),

    # 客户等级费用查询、修改、删除
    path('customerlevelfee_list/', customerlevelfee_list, name='customerlevelfee_list'),
    path('customerlevelfee_edit/<int:id>/', customerlevelfee_edit, name='customerlevelfee_edit'),
    path('customerlevelfee_del/<int:id>/', customerlevelfee_del, name='customerlevelfee_del'),

    # 公司费用列表查询
    path('companyfee_list/', companyfee_list, name='companyfee_list'),
    # 公司费用编辑
    path('companyfee_edit/<int:id>/', companyfee_edit, name='companyfee_edit'),
    #单个公司费用清单
    path('companyfee_item/<int:id>/', companyfee_item, name='companyfee_item'),

    path('query_bill/<int:id>', query_bill, name='query_bill'),

    #公告查询、修改、删除
    path('announcement_list/',announcement_list,name='announcement_list'),
    path('announcement_edit/<int:id>/',announcement_edit,name='announcement_edit'),
    path('announcement_del/<int:id>/',announcement_del,name='announcement_del'),

    #显示公告内容
    path('announcement_item/<int:id>/', cache_page(60 * 60)(announcement_item), name='announcement_item'),
    #公告批量操作
    path('announcement_batch_del/',announcement_batch_del,name='announcement_batch_del'),


    #Sku的增删改查
    path('sku_list/', sku_list, name='sku_list'),
    path('sku_list_company', sku_list_company, name='sku_list_company'),
    path('sku_list_company_item/<int:id>',sku_list_company_item, name='sku_list_company_item'),
    path('sku_create/', sku_create, name='sku_create'),
    path('sku_edit/<int:id>/', sku_edit, name='sku_edit'),
    path('sku_del/<int:id>/', sku_del, name='sku_del'),

    #仓库管理员审核SKU
    path('sku_examine_list/', sku_examine_list, name='sku_examine_list'),
    path('sku_examine_edit/<int:id>/', sku_examine_edit, name='sku_examine_edit'),

    #从到货核查进入Sku编辑
    path('sku_check_again/<int:sku_id>/<int:trans_id>/', sku_check_again, name='sku_check_again'),

    #管理员SKU数量修改
    path('sku_count_edit/<int:id>', sku_count_edit, name='sku_count_edit'),

    path('download_skus/', download_skus, name='download_skus'),

    #预报运单查询、修改、删除、提交
    path('transorder_list/', transorder_list, name='transorder_list'),
    path('transorder_list_company/', transorder_list_company, name='transorder_list_company'),
    path('transorder_list_company_item/<int:id>/', transorder_list_company_item, name='transorder_list_company_item'),
    path('transorder_create/', transorder_create, name='transorder_create'),
    path('transorder_edit/<int:id>/', transorder_edit, name='transorder_edit'),
    path('transorder_del/<int:id>', transorder_del, name='transorder_del'),
    path('transorder_submit/<int:id>', transorder_submit, name='transorder_submit'),
    # 核对运单的列表
    path('transorder_check_list/', transorder_check_list, name='transorder_check_list'),
    # 核对单个运单的查询、修改、删除
    path('transorder_check_edit/<int:id>/', transorder_check_edit, name='transorder_check_edit'),
    # 预报运单完结
    path('transorder_close/<int:id>', transorder_close, name='transorder_close'),
    # 查看已完结的运单
    path('transorder_look_over/<int:id>/', transorder_look_over, name='transorder_look_over'),
    # ajax获取sku的状态
    path('get_sku_status', get_sku_status, name='get_sku_status'),

    #仓租费编辑
    path('storagefee_list', storagefee_list, name='storagefee_list'),
    path('storagefee_create', storagefee_create, name='storagefee_create'),
    path('storagefee_edit/<int:id>/', storagefee_edit, name='storagefee_edit'),
    path('storagefee_del/<int:id>/', storagefee_del, name='storagefee_del'),

    path('download_prepayrecotd/<int:id>', download_prepayrecord, name='download_prepayrecord'),
    path('download_bill/<int:id>/<int:year>/<int:month>/<str:type>/', download_bill, name='download_bill'),
    # #预报运单中货物数量的查询、修改、删除,jquery动态添加运单内货物，但是bug较多
    # path('transorder_sum/', transorder_sum, name='transorder_sum'),

    # 库存变动查询
    path('stockchange_list', stockchange_list, name='stockchange_list'),

]
