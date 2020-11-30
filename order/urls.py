from django.urls import path
from .views import *

urlpatterns = [
    # 订单列表
    path('order_list/', order_list, name='order_list'),
    path('order_list_over/', order_list_over, name='order_list_over'),
    path('order_list_todo/', order_list_todo, name='order_list_todo'),
    path('download_orders/', download_orders, name='download_orders'),
    path('order_create/', order_create, name='order_create'),
    path('order_edit/<int:id>/', order_edit, name='order_edit'),
    path('order_del/<int:id>/', order_del, name='order_del'),
    #  从文件导入订单
    path('order_import/', order_import, name='order_import'),
    # 提交订单页面
    path('order_commit/<int:id>/', order_commit, name='order_commit'),
    # 处理订单
    path('order_deal/<int:id>/', order_deal, name='order_deal'),
    # 标注问题订单
    path('order_trouble/<int:id>/', order_trouble, name='order_trouble'),
    # # 订单出库
    # path('order_out/<int:id>/', order_over, name='order_out'),
    # 订单完结
    path('order_over/<int:id>/', order_over, name='order_over'),
    # 订单取消
    path('order_cancel/<int:id>/', order_cancel, name='order_cancel'),
    # 合并订单
    path('merge_orders/', merge_orders, name='merge_orders'),
    # 客户页面批量操作
    path('batch_orders_client/', batch_orders_client, name='batch_orders_client'),
    # 订单导出
    path('order_export/', order_export, name='order_export'),
    # 修改物流单号
    path('order_change_delivery_code/<int:id>/', order_change_delivery_code, name='order_change_delivery_code'),
    path('order_list_company', order_list_company, name='order_list_company'),
    path('order_list_status', order_list_status, name='order_list_status'),
    # path('order_list_company_item/<str:id>/<str:status>', order_list_company_item, name='order_list_company_item'),

    # 物流方案新建、修改、删除
    path('delivery_list/', delivery_list, name='delivery_list'),
    path('delivery_edit/<int:id>', delivery_edit, name='delivery_edit'),
    path('delivery_del/<int:id>', delivery_del, name='delivery_del'),
    # 客户查看可用物流方案
    path('delivery_query_list', delivery_query_list, name='delivery_query_list'),
    # 退件
    path('reject_list/', reject_list, name='reject_list'),
    path('reject_list_company/', reject_list_company, name='reject_list_company'),
    path('reject_list_company_item/<int:id>', reject_list_company_item, name='reject_list_company_item'),
    path('reject_create/', reject_create, name='reject_create'),
    path('reject_edit/<int:id>', reject_edit, name='reject_edit'),
    path('reject_del/<int:id>', reject_del, name='reject_del'),
    # 退件完结
    path('reject_over/<int:id>', reject_over, name='reject_over'),

    # 特殊邮编
    path('orderspecial_list', orderspecial_list, name='orderspecial_list'),
    path('orderspecial_create', orderspecial_create, name='orderspecial_create'),
    path('orderspecial_edit/<int:id>/', orderspecial_edit, name='orderspecial_edit'),
    path('orderspecial_del/<int:id>/', orderspecial_del, name='orderspecial_del'),


]