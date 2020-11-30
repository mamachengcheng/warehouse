from django.urls import path


from . import views


app_name = 'backend'
urlpatterns = [
    #后台首页
    path('', views.backend, name='index'),

    #销售查询
    path('sales_query', views.sales_query, name='sales_query'),

    #分段查询SKU销量
    path('query_time_delta', views.query_time_delta, name='query_time_delta'),

    #SKU低库存报警
    path('query_low_stock', views.query_low_stock, name='query_low_stock'),

    #仓租计算
    path('storage_fee_list', views.storage_fee_list, name='storage_fee_list')
]
