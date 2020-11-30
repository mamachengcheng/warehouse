from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
import xlwt


from account.models import Operation, Announcement, Companyvolumeperday
from .forms import *
from depot.models import Sku, Transorder
from order.models import Order, Reject
from account.models import Account, Company


# Create your views here.
@login_required()
def backend(request):
    #操作记录
    operate_record = Operation.objects.filter(account_id=request.user.id).order_by('-action_time')[:5]
    #公告
    announcements = Announcement.objects.filter(status=2).order_by('-publish_time')[:5]
    if request.user.is_staff:
        todo = {}
        skus_sum = Sku.objects.all().count()
        skus_check_sum = Sku.objects.filter(status='0').count()
        trans = Transorder.objects.all().count()
        trans_to_submit = Transorder.objects.filter(status_trans='2').count()
        orders = Order.objects.all().count()
        orders_to_check = Order.objects.filter(status='2').count()
        orders_to_out = Order.objects.filter(status='3').count()
        orders_over = Order.objects.filter(status='4').count()
        rejects = Reject.objects.all().count()
        rejects_todo = Reject.objects.filter(status='1').count()
        tudo = {
            'skus_sum': skus_sum, 'skus_check_sum': skus_check_sum,
            'trans': trans, 'trans_to_submit': trans_to_submit,
            'orders': orders, 'orders_to_check': orders_to_check,
            'orders_to_out': orders_to_out,'orders_over':orders_over,
            'rejects': rejects, 'rejects_todo': rejects_todo
        }
        depot = {}
        company_sum = Company.objects.all().count()
        accounts = Account.objects.filter(is_staff=True).count()
        prepay_total = Company.objects.all().aggregate(Sum('prepayment'))
        depot = {
            'company_sum':company_sum,'accounts':accounts,'prepay_total':prepay_total['prepayment__sum'],
        }
    else:
        #事务相关数据统计
        todo = {}
        company = request.user.company
        skus_sum = Sku.objects.filter(company=company).count()
        skus_check_sum = Sku.objects.filter(company=company,status='0').count()
        trans = Transorder.objects.filter(company=company).count()
        trans_to_submit = Transorder.objects.filter(company=company, status_trans='1').count()
        orders = Order.objects.filter(company=company).count()
        orders_to_submit = Order.objects.filter(company=company,status='1').count()
        orders_problem = Order.objects.filter(company=company,status='6').count()
        rejects = Reject.objects.filter(company=company).count()
        rejects_todo = Reject.objects.filter(company=company,status='1').count()
        tudo = {
            'skus_sum':skus_sum,'skus_check_sum':skus_check_sum,
            'trans':trans, 'trans_to_submit':trans_to_submit,
            'orders':orders,'orders_to_submit':orders_to_submit,'orders_problem':orders_problem,
            'rejects':rejects,'rejects_todo':rejects_todo
        }
        #仓库相关统计
        depot = {}
        now = timezone.now()
        vol_current = company.get_volume_per_day()
        vol_out = company.get_volume_out_month(year=now.year,month=now.month)
        prepay = company.prepayment
        level = company.level
        accounts = Account.objects.filter(company=company).count()
        depot = {
            'vol_current':vol_current,'vol_out':vol_out,'prepay':prepay,
            'level':level,'accounts':accounts,
        }
    return render(request, template_name='backend_index.html',context={
        'op': operate_record,
        'anno': announcements,
        'todo': tudo,
        'depot': depot,
    })


@login_required()
def sales_query(request):
    time_form = QueryTimeDeltaForm()
    low_form = QueryLowStockForm()
    if request.user.is_staff:
        time_form.fields['sku'].queryset = Sku.objects.all()
        # low_form.fields['sku'].queryset = Sku.objects.all()
    else:
        time_form.fields['sku'].queryset=Sku.objects.filter(company=request.user.company)
        # low_form.fields['sku'].queryset = Sku.objects.filter(company=request.user.company)
    return render(request,'sales_query.html',{'time_form':time_form,'low_form':low_form})


@login_required()
def query_time_delta(request):
    time_form = QueryTimeDeltaForm(request.GET)
    if time_form.is_valid():
        #获取选择的时间
        #开始日期
        begin_date = time_form.cleaned_data['begin_date']

        # from django.utils import timezone
        # begin_date = timezone.make_aware(begin_date,timezone.get_current_timezone())

        #结束日期
        end_date = time_form.cleaned_data['end_date']
        #SKU对象
        sku = time_form.cleaned_data['sku']
        #指定时间段内总入库量
        in_sum = sku.stockchange_set.filter(change_type='1', change_time__gte=begin_date,
                                            change_time__lte=end_date).aggregate(Sum('quantity'))
        if in_sum['quantity__sum'] :
            in_sum = in_sum['quantity__sum']
        else:
            in_sum = 0
        #指定时间段内总出库量
        out_sum = sku.stockchange_set.filter(change_type='2', change_time__gte=begin_date,
                                            change_time__lte=end_date).aggregate(Sum('quantity'))
        if out_sum['quantity__sum'] :
            out_sum = out_sum['quantity__sum']
        else:
            out_sum = 0

        #出入库总量比值
        if out_sum == 0:
            in_out_ratio = 0
        else:
            in_out_ratio = in_sum / out_sum
            in_out_ratio = float('%.2f' % in_out_ratio)
        #区间日期数量
        delta_data = end_date - begin_date
        delta_data = delta_data.days
        if delta_data < 0:
            delta_data = -delta_data
        # 当前库存
        cur_sum = sku.get_current_normal()

        #日均销量
        if delta_data == 0:
            avg_sum = 0
        else:
            avg_sum = out_sum / delta_data
            avg_sum = float('%.2f' % avg_sum)

        if avg_sum == 0:
            sales_days = 0
        else:
            sales_days = cur_sum / avg_sum
            sales_days = float('%.2f' % sales_days)
        recent_3 = sku.sales_delta(3)
        recent_7 = sku.sales_delta(7)
        recent_14 = sku.sales_delta(14)
        recent_30 = sku.sales_delta(30)
        recent_90 = sku.sales_delta(90)
        return render(request, 'query_time_delta.html', {
            'sku':sku,
            'begin_date':begin_date,
            'end_date':end_date,
            'delta_data':delta_data,
            'in_sum': in_sum,
            'out_sum': out_sum,
            'avg_sum': avg_sum,
            'in_out_ratio': in_out_ratio,
            'sales_days': sales_days,
            'out_3': recent_3['out_sum'],
            'avg_3': recent_3['avg_sales'],
            'out_7': recent_7['out_sum'],
            'avg_7': recent_7['avg_sales'],
            'out_14': recent_14['out_sum'],
            'avg_14': recent_14['avg_sales'],
            'out_30': recent_30['out_sum'],
            'avg_30': recent_30['avg_sales'],
            'out_90': recent_90['out_sum'],
            'avg_90': recent_90['avg_sales'],
        })


@login_required()
def query_low_stock(request):
    quantity = request.GET['quantity']
    if request.user.is_staff:
        skus = Sku.objects.all()
    else:
        skus = Sku.objects.filter(company=request.user.company)
    result = []
    for item in skus:
        if item.get_current_normal() < int(quantity):
            result.append(item)
    return render(request, 'query_low_stock.html', {'result':result,'quantity':quantity})


@login_required()
def storage_fee_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            volumes = Companyvolumeperday.objects.all()
            storage_form = QueryStorageForm()
        else:
            volumes = Companyvolumeperday.objects.filter(company=request.user.company)
            storage_form = QueryStorageForm()
        return render(request,'storage_fee_list.html',{'volumes':volumes, 'storage_form': storage_form})
    elif request.method == 'POST':
        storage_form = QueryStorageForm(request.POST)
        if storage_form.is_valid():
            # 开始日期
            begin_date = storage_form.cleaned_data['begin_date']
            # 结束日期
            end_date = storage_form.cleaned_data['end_date']
            # 操作类型
            type = request.POST['type']
            if request.user.is_staff:
                volumes = Companyvolumeperday.objects.filter(date__gte=begin_date, date__lte=end_date)
            else:
                volumes = Companyvolumeperday.objects.filter(date__gte=begin_date, date__lte=end_date,
                                                             company=request.user.company)
            if type == '查询':
                return render(request, 'storage_fee_list.html', {'volumes': volumes, 'storage_form': storage_form})
            if type == '导出目前查询的数据':
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename=prepayrecord.xls'
                workbook = xlwt.Workbook(encoding='utf-8')
                sheet = workbook.add_sheet('sheet1')
                row0 = ['序号', '记录时间', '公司名称', '当日库存体积', '当日出库体积']
                for i in range(0, len(row0)):
                    sheet.write(0, i, row0[i])
                row = 1
                for i in range(0, len(volumes)):
                    sheet.write(row, 0, i + 1)
                    sheet.write(row, 1, volumes[i].date.strftime('%Y-%m-%d %H:%M:%S'))
                    sheet.write(row, 2, volumes[i].company.name)
                    sheet.write(row, 3, volumes[i].volume)
                    sheet.write(row, 4, volumes[i].out)
                    row = row + 1
                workbook.save(response)
                return response
        else:
            return render(request, 'storage_fee_list.html', {'volumes': request.POST['volumes'], 'storage_form': storage_form})


# def read_file(filename,chunk_size=512):
#     with open(filename, 'rb') as f:
#         while True:
#             block=f.read(chunk_size)
#             if block:
#                 yield block
#             else:
#                 break
# response['Content-Type'] = 'application/octet-stream'
    # response['Content-Type'] = 'application/vnd.ms-excel'

# def download_file(request):
#     response = StreamingHttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment;filename=export.xls'
#     return response
