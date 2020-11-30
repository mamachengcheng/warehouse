import xlrd,xlwt
import csv
import random
from django.utils import timezone
from decimal import Decimal
import json
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


from account.models import Operation, Prepayrecord, Company
from depot.models import Sku, Count, Customerlevelfee, Depot
from .models import Order, Ordercontain, Ordercomment, Delivery, Reject, Rejectcontain, Orderspecial
from .forms import *
from depot.views import stock_change, change_type
from depot.forms import SelectCompanyForm



# Create your views here.
def create_order_code():
    d = timezone.now()
    prefix = d.strftime("%y%m%d%H%M%S")
    tail = random.randrange(100000, 999999)
    return prefix + str(tail)


@login_required()
def order_list_over(request):
    # 已完成订单列表，因为查询可以分订单状态，这个就不需要了
    data = Order.objects.filter(status='5')
    special_postcode = Orderspecial.all_special_postcode()
    content_type = ContentType.objects.get_for_model(Order)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request, 'order_list.html', {'data':data,'op':operate_record,'special_postcode':special_postcode})


@login_required()
def merge_orders(request):
    order_id_list = request.GET['data'].split(",")
    parent_order = get_object_or_404(Order,pk=order_id_list[0])
    if parent_order.status == '1':
        merge = 0
        for i in range(1,len(order_id_list)):
            order = get_object_or_404(Order,pk=order_id_list[i])
            if(parent_order.company == order.company and parent_order.depot == order.depot and
               # parent_order.sales_record_number == order.sales_record_number and
                       parent_order.user_id == order.user_id and
               parent_order.buyer_full_name == order.buyer_full_name and parent_order.buyer_phone_number == order.buyer_phone_number
               and parent_order.buyer_email == order.buyer_email and parent_order.buyer_postcode == order.buyer_postcode and
               parent_order.buyer_city == order.buyer_city and parent_order.buyer_county == order.buyer_county and
               parent_order.buyer_country == order.buyer_country and parent_order.buyer_address1 == order.buyer_address1 and
               parent_order.buyer_address2 == order.buyer_address2 and parent_order.status == order.status):
                contain = order.ordercontain_set.last()
                contain.order = parent_order
                contain.save()
                order.delete()
                merge += 1
        if merge > 0:
            merge += 1
            msg = '共有' + str(len(order_id_list)) + '个订单进行合并，其中' + str(merge) + '个合并成功，合并后的订单号为：' + parent_order.order_code
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            msg = '订单合并失败，请确认待合并的订单信息！'
            messages.add_message(request, messages.ERROR, msg)
    else:
        msg = '只能合并未提交的订单！'
        messages.add_message(request, messages.ERROR, msg)
    return redirect('order_list')


@login_required()
def batch_orders_client(request):
    order_id_list = request.GET['data'].split(",")
    operate = request.GET['operate']
    op = 0
    if operate == '1':
        for i in range(len(order_id_list)):
            order = get_object_or_404(Order, pk=order_id_list[i])
            if order.status == '1' or order.status == '6':
                order.status = '2'
                order.save()
                Operation.objects.create(account=request.user, action='3', description='提交订单', content_object=order,
                                         object_repr=order)
                op = op + 1
        msg = "成功提交" + str(op) + "个订单"
        messages.add_message(request, messages.SUCCESS, msg)
    elif operate == '2':
        for i in range(len(order_id_list)):
            order = get_object_or_404(Order, pk=order_id_list[i])
            if order.status == '1' or order.status == '6':
                Operation.objects.create(account=request.user, action='2', description='删除订单', content_object=order,
                                         object_repr=order)
                order.delete()
                op = op + 1
        msg = "成功删除" + str(op) + "个订单"
        messages.add_message(request, messages.SUCCESS, msg)
    else:
        pass
    return redirect('order_list')


@login_required()
def download_orders(request):
    #导出csv格式
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=order.csv'
    writer = csv.writer(response)
    order_id_list = request.GET['data'].split(",")
    for n in range(0, len(order_id_list)):
        row_content = []
        data = get_object_or_404(Order,pk=int(order_id_list[n]))
        # sheet.write(row, 0, i+1)
        row_content.append(data.buyer_full_name)
        row_content.append(data.buyer_address1)
        row_content.append(data.buyer_address2)
        row_content.append(data.buyer_postcode)
        row_content.append(data.buyer_city)
        row_content.append(data.buyer_country)
        row_content.append(data.buyer_phone_number)
        row_content.append(data.sales_record_number)
        row_content.append(data.order_code)
        skus = data.ordercontain_set.all()
        sku_label = ""
        units = ""
        quantity = ""
        weight = ""
        i = 0
        for item in skus:
            sku_label += item.sku.code
            units += item.sku.count_set.last().unit.name
            quantity += str(item.amount)
            weight += str(item.sku.weight)
            i += 1
            if i < len(skus):
                sku_label += " / "
                units += " / "
                quantity += " / "
                weight += " / "
        row_content.append(sku_label)
        row_content.append(units)
        row_content.append(quantity)
        row_content.append(weight)

        writer.writerow(row_content)
    return response
# def download_orders(request):
#     # TODO 订单sku库位的仓库未处理
#     # 导出待处理订单excel格式
#     # jquery的get，post方法传来的参数都得用getlist来获取
#     # js构造表单提交的可以直接字典方式获取
#     order_id_list = request.GET['data'].split(",")
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment;filename=order.xls'
#     workbook = xlwt.Workbook(encoding='utf-8')
#     sheet = workbook.add_sheet('sheet1')
#     # 表头，订单导出时可以去掉，去掉后记得改后面的行号
#     # row0 = ['序号', '消费者姓名', '地址1', '地址2', '邮编', '城市', '国家', '联系电话', '客户系统订单号',
#     #         '雷欧订单号', '客户SKU', '库位', '数量', '重量']
#     # for i in range(0, len(row0)):
#     #     sheet.write(0, i, row0[i])
#     # 从第一行开始依次写入数据
#     # 包含的SKU要合并在一个单元各内
#     row = 0
#     for i in range(0, len(order_id_list)):
#         data = get_object_or_404(Order,pk=int(order_id_list[i]))
#         # sheet.write(row, 0, i+1)
#         sheet.write(row, 0, data.buyer_full_name)
#         sheet.write(row, 1, data.buyer_address1)
#         sheet.write(row, 2, data.buyer_address2)
#         sheet.write(row, 3, data.buyer_postcode)
#         sheet.write(row, 4, data.buyer_city)
#         sheet.write(row, 5, data.buyer_country)
#         sheet.write(row, 6, data.buyer_phone_number)
#         sheet.write(row, 7, data.sales_record_number)
#         sheet.write(row, 8, data.order_code)
#         skus = data.ordercontain_set.all()
#         sku_label = ""
#         units = ""
#         quantity = ""
#         weight = ""
#         i = 0
#         for item in skus:
#             sku_label += item.sku.code
#             units += item.sku.count_set.last().unit.name
#             quantity += str(item.amount)
#             weight += str(item.sku.weight)
#             i += 1
#             if i < len(skus):
#                 sku_label += " / "
#                 units += " / "
#                 quantity += " / "
#                 weight += " / "
#         sheet.write(row, 9, sku_label)
#         sheet.write(row, 10, units)
#         sheet.write(row, 11, quantity)
#         sheet.write(row, 12, weight)
#
#         row = row + 1
#     workbook.save(response)
#     return response

@login_required()
def order_list(request):
    #订单列表
    # if request.user.is_staff:
    #     data = Order.objects.exclude(status__in=['1','6'])
    #     operate_record = Operation.objects.filter(content_type_id=20).order_by('-action_time')[:10]
    # else:
    search = request.GET.get('search')
    if search:
        data = Order.objects.filter(company=request.user.company).filter(
            Q(sales_record_number__icontains=search) | Q(order_code__icontains=search) | Q(delivery_code__icontains=search)
        ).order_by('-id')
    else:
        data = Order.objects.filter(company=request.user.company).order_by('-id')

    special_postcode = Orderspecial.all_special_postcode()
    content_type = ContentType.objects.get_for_model(Order)
    select_status = SelectStatusForm(initial={'status': '8'})
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'order_list.html', {'contacts':contacts,'search':search,
                                               'op':operate_record,
                                               'select_status':select_status,
                                               'special_postcode':special_postcode})


@login_required()
def order_list_status(request):
    special_postcode = Orderspecial.all_special_postcode()
    content_type = ContentType.objects.get_for_model(Order)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    status = request.GET['status']
    if status == '8':
        data = Order.objects.filter(company=request.user.company).order_by('-id')
    else:
        data = Order.objects.filter(company=request.user.company,status=status).order_by('-id')
    select_status = SelectStatusForm(initial={'status':status})
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'order_list.html',
                  {'contacts': contacts, 'op': operate_record, 'special_postcode': special_postcode,
                   'select_status': select_status, 'status':status})


@login_required()
def order_list_todo(request):
    #订单列表
    search = request.GET.get('search')
    if search:
        data = Order.objects.exclude(status__in=['1', '6']).filter(
            Q(sales_record_number__icontains=search) | Q(order_code__icontains=search) | Q(delivery_code__icontains=search)
            ).order_by('-id')
    else:
        data = Order.objects.exclude(status__in=['1','6']).order_by('-id')
    special_postcode = Orderspecial.all_special_postcode()
    content_type = ContentType.objects.get_for_model(Order)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    select_company = SelectCompanyAndStatusForm()
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'order_list_todo.html', {'contacts':contacts,'op':operate_record,
                                                    'special_postcode':special_postcode,'select_company':select_company,
                                                    'search':search})


@login_required()
def order_list_company(request):
    special_postcode = Orderspecial.all_special_postcode()
    content_type = ContentType.objects.get_for_model(Order)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    company = request.GET['company']
    status = request.GET['status']
    if company == '':
        if status == '1':
            data = Order.objects.all().exclude(status__in=['1', '6']).order_by('-id')
        else:
            data = Order.objects.filter(status=status).exclude(status__in=['1', '6']).order_by('-id')
    else:
        if status == '1':
            data = Order.objects.filter(company=company).exclude(status__in=['1', '6']).order_by('-id')
        else:
            data = Order.objects.filter(company=company, status=status).exclude(status__in=['1', '6']).order_by('-id')
    select_company = SelectCompanyAndStatusForm(initial={'company': company,'status':status})
    back = company
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'order_list_todo.html',
                  {'contacts': contacts, 'op': operate_record, 'special_postcode': special_postcode,
                   'select_company': select_company, 'back':back, 'status':status,
                   'selected_company_id': request.GET['company'], 'select_status_id': request.GET['status']})


@login_required()
def order_export(request):
    if request.method == 'GET':
        order_export_form = ExportOrderForm()
        return render(request, 'order_export.html', {'order_export_form':order_export_form})
    else:
        # 导出订单excel格式
#     # jquery的get，post方法传来的参数都得用getlist来获取
#     # js构造表单提交的可以直接字典方式获取
#     order_id_list = request.GET['data'].split(",")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=order_delta.xls'
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('sheet1')
        order_export_form = ExportOrderForm(request.POST)
        if order_export_form.is_valid():
            # 获取选择的时间
            # 开始日期
            begin_date = order_export_form.cleaned_data['begin_date']
            # 结束日期
            end_date = order_export_form.cleaned_data['end_date']
            # 要导出的订单状态
            status = order_export_form.cleaned_data['status']
            if request.user.is_staff:
                if status == '8':
                    orders = Order.objects.filter(create_time__gte=begin_date, create_time__lte=end_date)
                else:
                    orders = Order.objects.filter(create_time__gte=begin_date, create_time__lte=end_date, status=status)
            else:
                if status == '8':
                    orders = Order.objects.filter(company=request.user.company, create_time__gte=begin_date, create_time__lte=end_date)
                else:
                    orders = Order.objects.filter(company=request.user.company, create_time__gte=begin_date, create_time__lte=end_date, status=status)
            # 表头，订单导出时可以去掉，去掉后记得改后面的行号
            row0 = ['序号', '消费者姓名', '地址1', '地址2', '邮编', '城市', '国家', '联系电话', '客户系统订单号',
                    '雷欧订单号', '客户SKU', '库位', '数量', '重量', '物流服务商中文名称','物流服务商英文名称',
                    '物流服务单号', '订单操作费', '订单最终运费', '订单状态', '订单创建日期']
            for i in range(0, len(row0)):
                sheet.write(0, i, row0[i])
            # 从第一行开始依次写入数据
            # 包含的SKU要合并在一个单元各内
            row = 1
            for i in range(0, len(orders)):
                data = orders[i]
                sheet.write(row, 0, i+1)
                sheet.write(row, 1, data.buyer_full_name)
                sheet.write(row, 2, data.buyer_address1)
                sheet.write(row, 3, data.buyer_address2)
                sheet.write(row, 4, data.buyer_postcode)
                sheet.write(row, 5, data.buyer_city)
                sheet.write(row, 6, data.buyer_country)
                sheet.write(row, 7, data.buyer_phone_number)
                sheet.write(row, 8, data.sales_record_number)
                sheet.write(row, 9, data.order_code)
                skus = data.ordercontain_set.all()
                sku_label = ""
                units = ""
                quantity = ""
                weight = ""
                i = 0
                for item in skus:
                    sku_label += item.sku.code
                    units += item.sku.count_set.last().unit.name
                    quantity += str(item.amount)
                    weight += str(item.sku.weight)
                    i += 1
                    if i < len(skus):
                        sku_label += " / "
                        units += " / "
                        quantity += " / "
                        weight += " / "
                sheet.write(row, 10, sku_label)
                sheet.write(row, 11, units)
                sheet.write(row, 12, quantity)
                sheet.write(row, 13, weight)
                if data.delivery_service:
                    sheet.write(row, 14, data.delivery_service.name)
                    sheet.write(row, 15, data.delivery_service.name_en)
                    sheet.write(row, 16, data.delivery_code)
                else:
                    sheet.write(row, 14, '')
                    sheet.write(row, 15, '')
                    sheet.write(row, 16, '')
                sheet.write(row, 17, data.get_op_fee())
                sheet.write(row, 18, data.final_delivery_fee)
                sheet.write(row, 19, data.get_status_display())
                sheet.write(row, 20, str(data.create_time))
                row = row + 1
            workbook.save(response)
            return response

# @login_required()
# @permission_required('order.add_order', raise_exception=True)
def order_create(request):
    # 在OrderContainFormSet中进行库存校验
    # 校验订单中的SKU库存是否充足
    # 邮编校验
    # 先确定用户预存款余额大于100
    if request.user.company.prepayment < 100:
        return redirect('backend:index')

        # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(company=request.user.company, status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])

    if request.method == 'GET':
        form = OrderForm(initial={'company': request.user.company,'order_code':create_order_code(),'depot':Depot.current()})
        form.fields['delivery_service'].queryset = Delivery.objects.filter(level=request.user.company.level)
        return render(request, 'order_create.html', {'form': form, 'sku_code_list':sku_belongs_to_company})

    else:
        new = OrderForm(request.POST)
        # 解析post，用的很笨的办法
        # result = []
        result = {}
        for n in range(len(request.POST)):
            index_s = "sku_code_" + str(n)
            index_a = "amount_" + str(n)
            if index_s in request.POST:
                result[request.POST[index_s]] = request.POST[index_a]

        if new.is_valid():
            log = new.save(commit=False)
            # 对结果进行处理
            # 错误列表
            # 检查SKU是否正确、是否有足够的数量
            errors = []
            for key, value in result.items():
                try:
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    sum = Count.objects.get(sku=sku)
                    if sum.normal < int(value):
                        error = "SKU:" + key + "数量不足，请重新检查"
                        errors.append(error)
                except:
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                new.fields['delivery_service'].queryset = Delivery.objects.filter(level=request.user.company.level)
                return render(request, 'order_create.html', {
                    'form': new,
                    'data': change_type(result,request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                })
            else:
                log.order_code = create_order_code()
                log.save()
                for key, value in result.items():
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    Ordercontain.objects.create(order=log, sku=sku, amount=int(value))
                messages.add_message(request, messages.SUCCESS, '新订单创建成功！')
                Operation.objects.create(account=request.user, action='1', description='创建新订单', content_object=log,
                                         object_repr=log)
                return redirect('/order_list_status?status=1')
        else:
            new.fields['delivery_service'].queryset = Delivery.objects.filter(level=request.user.company.level)
            return render(request, 'order_create.html', {
                    'form': new,
                    'data':change_type(result,request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,})


@login_required()
@permission_required('order.change_order', raise_exception=True)
def order_edit(request,id):
    old = get_object_or_404(Order, pk=id)
    # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(company=request.user.company, status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])
    # 获取运单SKU信息
    skus = Ordercontain.objects.filter(order=old)
    data = {}
    for item in skus:
        data[item.sku.code] = item.amount

    if request.method == 'POST':
        new = OrderForm(request.POST, instance=old)
        # 解析post，用的很笨的办法
        # result = []
        result = {}
        for n in range(len(request.POST)):
            index_s = "sku_code_" + str(n)
            index_a = "amount_" + str(n)
            if index_s in request.POST:
                result[request.POST[index_s]] = request.POST[index_a]

        if new.is_valid():
            # 对结果进行处理
            # 错误列表
            # 检查SKU是否正确、是否有足够的数量
            errors = []
            for key, value in result.items():
                try:
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    sum = Count.objects.get(sku=sku)
                    if sum.normal < int(value):
                        error = "SKU:" + key + "数量不足，请重新检查"
                        errors.append(error)
                except:
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                return render(request, 'order_edit.html', {
                    'form': new,
                    'data': change_type(result, request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                    'status': request.POST['status'],
                })
            else:
                log = new.save()
                preds = Ordercontain.objects.filter(order=log)
                for p in preds:
                    p.delete()
                for key, value in result.items():
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    Ordercontain.objects.create(order=log, sku=sku, amount=int(value))
                messages.add_message(request, messages.SUCCESS, '订单修改成功！')
                Operation.objects.create(account=request.user, action='3', description='修改订单', content_object=log,
                                         object_repr=log)

                if request.POST['status']:
                    return redirect('/order_list_status?status=' + request.POST['status'])
                else:
                    return redirect('order_list')
        else:
            new.fields['delivery_service'].queryset = Delivery.objects.filter(level=request.user.company.level)
            return render(request, 'order_edit.html', {'form': new, 'id': id, 'data':change_type(result,request.user.company),
                                                        'sku_code_list': sku_belongs_to_company,'status':request.POST['status']})
    else:
        form = OrderForm(instance=old)
        form.fields['delivery_service'].queryset = Delivery.objects.filter(level=request.user.company.level)
        return render(request, 'order_edit.html', {'form': form, 'id': id, 'data':change_type(data,request.user.company),
                                                        'sku_code_list': sku_belongs_to_company,'status':request.GET['status']})


@login_required()
@permission_required('order.delete_order', raise_exception=True)
def order_del(request,id):
    log = get_object_or_404(Order,pk=id)
    Operation.objects.create(account=request.user, action='2', description='删除订单', content_object=log,
                             object_repr=log)
    log.delete()
    messages.add_message(request, messages.SUCCESS, '订单删除成功！')
    if request.POST['status']:
        return redirect('/order_list_status?status='+request.POST['status'])
    else:
        return redirect('order_list')


@login_required()
@permission_required('order.add_order', raise_exception=True)
def order_import(request):
    # 订单从excel导入
    # TODO 未做模板错误处理
    if request.user.company.prepayment < 100:
        return redirect('backend:index')
    if request.method == 'POST':
        form = OrderImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('excel_file','')
            if file:
                try:
                    data = xlrd.open_workbook(filename=None,file_contents=file.read())
                except:
                    return render(request, 'order_import.html', {'form': form})
                table = data.sheets()[0]
                nrows = table.nrows
                ncols = table.ncols
                colnames = table.row_values(0)
                list = []
                for row_num in range(1,nrows):
                    row = table.row_values(row_num)
                    if row:
                        each_order = {}
                        for i in range(len(colnames)):
                            each_order[colnames[i]] = row[i]
                        list.append(each_order)
                result = batch_order(request, list)
                if result['success'] > 0:
                    messages.add_message(request, messages.SUCCESS, '新订单创建成功！')
                data = Order.objects.filter(company=request.user.company)
                content_type = ContentType.objects.get_for_model(Order)
                operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
                special_postcode = Orderspecial.all_special_postcode()
                return render(request, 'order_list.html', {'data': data, 'op': operate_record, 'result':result,
                                                           'special_postcode':special_postcode})
            else:
                return render(request, 'order_import.html', {'form': form})
    else:
        form = OrderImportForm()
        return render(request, 'order_import.html', {'form':form})


@login_required()
def batch_order(request, list):
    #EXCEL文件导入订单的处理
    #TODO 在前端就要做，大小，文件名都要限制，后台再校验excel文件的格式是否符合模板要求
    company = request.user.company
    depot = Depot.current()
    error_list = []
    success = 0
    error = 0
    warn = 0
    merge = 0
    total = 0
    for i in list:
        total += 1
        #校验SKU代码是否存在
        # excel读入数字会变成float格式，末尾带上.0，直接转str会有问题
        if isinstance(i['Custom Label'], str):
            custom_label = i['Custom Label']
        else:
            custom_label = str(int(i['Custom Label']))
        # custom_label = (str(i['Custom Label']).split('.')[0])
        try:
            sku_ok = Sku.objects.get(company=company, code=custom_label)
        except:
            error_msg = '客户平台订单号为：'+i['Sales Record Number']+'的SKU代码：'+custom_label+'不存在。'
            error_msg += '请检查SKU是否正确，或者是否已在海外仓系统中添加。'
            error_list.append(error_msg)
            error += 1
            continue
        # 校验SKU库存是否有库存
        # 现在sku创建后就会加入全是0的库存记录，这条验证失效了
        try:
            quantity_ok = Count.objects.get(sku=sku_ok)
        except:
            error_msg = '客户平台订单号为：' + i['Sales Record Number'] + '的SKU代码：' + custom_label + '没有库存。'
            error_msg += '请检查库存数量后再添加订单。'
            error_list.append(error_msg)
            error += 1
            continue
        #校验SKU库存是否充足
        if quantity_ok.normal < int(i['Quantity']):
            error_msg = '客户平台订单号为：' + i['Sales Record Number'] + '的SKU代码：' + custom_label + '库存不足。'
            error_msg += '请检查库存数量后再添加订单。'
            error_list.append(error_msg)
            error += 1
            continue
        #校验是否重复订单
        try:
            order_ok = Order.objects.get(sales_record_number=i['Sales Record Number'],user_id=i['User Id'],
                                         buyer_address1=i['Buyer Address 1'],status='1')
            amount_ok = order_ok.ordercontain_set.get(sku__code=custom_label)
            if amount_ok.amount == i['Quantity']:
                error_msg = '查询到有与客户平台订单号为：' + i['Sales Record Number'] + '内容相同的未提交订单。'
                error_msg += '请检查未提交订单中是否已包含此订单，或并修改订单内容后重新添加。'
                error += 1
                error_list.append(error_msg)
                continue
        except:
            pass
        #校验物流商是否正确，不正确提示警告，但订单可以创建
        try:
            delivery_ok = Delivery.objects.get(level=request.user.company.level, name=i['Delivery Service'])
        except:
            delivery_ok = None
            error_msg = '客户平台订单号为：' + i['Sales Record Number'] + '的物流商：' + str(i['Delivery Service']) + '不存在。'
            error_msg += '订单已创建，但请检查物流商名称并修改后再提交。'
            warn += 1
            error_list.append(error_msg)

        # print(i['Buyer Postcode'])
        # print(Orderspecial.all_special_postcode())
        change_postcode = str(int(i['Buyer Postcode']))
        if change_postcode in Orderspecial.all_special_postcode():
            error_msg = '客户平台订单号为：' + i['Sales Record Number'] + '的邮编：' + change_postcode + '属于偏远地区。'
            error_msg += '订单已创建，但请与管理员核实最终运费。'
            warn += 1
            error_list.append(error_msg)
        #创建订单
        #用这种方法也实现了合并，如果订单信息完全一致，就在订单基础上添加货物信息
        #因为客户导出excel说明原来订单是在一起的，自动合并即可
        # 这里取消了自动合并，改成创建后手动合并
        # log,created = Order.objects.get_or_create(company = company,
        log = Order.objects.create(company = company,
                                   # order_code = create_order_code(),
                             sales_record_number = i['Sales Record Number'],
                             user_id = i['User Id'],
                             buyer_full_name = i['Buyer Full name'],
                             buyer_phone_number = i['Buyer Phone Number'],
                             buyer_email = i['Buyer Email'],
                             buyer_address1 = i['Buyer Address 1'],
                             buyer_address2 = i['Buyer Address 2'],
                             buyer_city = i['Buyer Town/City'],
                             buyer_postcode = change_postcode,
                             buyer_county = i['Buyer County'],
                             buyer_country = i['Buyer Country'],
                             depot = depot,)
        # if not created:
        #     merge += 1
        #     Operation.objects.create(account=request.user, action='1', description='合并订单', content_object=log,
        #                          object_repr=log)
        #     Ordercontain.objects.create(order=log, sku=sku_ok, amount=i['Quantity'])
        #     success += 1
        # else:
        log.order_code = create_order_code()
        log.delivery_service = delivery_ok
        log.save()
        # 保存SKU及数量
        Ordercontain.objects.create(order=log, sku=sku_ok, amount=i['Quantity'])
        # 记录日志
        Operation.objects.create(account=request.user, action='1', description='创建新订单', content_object=log,
                                 object_repr=log)
        success += 1
    # if merge > 0:
    #     merge += 1
    result = {'error_list':error_list, 'total':total, 'success':success, 'error':error, 'warn':warn,}
    return result


#订单处理流程
#1.order_import OR order_edit   --->status='1'
#2.order_commit                 --->status='2'
#3.order_deal                   --->status='3' OR '6'
#4-1 status='6' EQUAL status='1'
#4-2 order_out                  --->status='4'
@login_required()
def order_commit(request,id):
    #订单提交，显示全部订单信息，确认后改变订单状态
    if request.method == 'POST':
        log = get_object_or_404(Order, pk=id)
        log.status = '2'
        log.save()
        Operation.objects.create(account=request.user, action='3', description='提交订单', content_object=log,
                                 object_repr=log)
        return redirect('/order_list_status?status=2')
        # return redirect('order_list')


@login_required()
@permission_required('order.change_order',raise_exception=True)
def order_deal(request,id):
    #处理已提交订单,录入物流单号，扣除操作费，确认最终重量
    #TODO 需要修改为处理后库存转入待出库
    item = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        #TODO 处理后订单运费的显示，在list中
        item.delivery_code = request.POST['delivery_code']
        item.final_weight = request.POST['final_weight']
        item.status = '3'
        item.save()
        company = item.company
        Prepayrecord.objects.create(company=company, account=request.user, sum=-item.operation_fee(), type=3,
                                    instruction='订单%s的操作费' % item.order_code, order=item)
        company.prepayment -= item.operation_fee()
        company.save()
        stock_change(request, type='out', order_id=id)
        Operation.objects.create(account=request.user, action='3', description='处理订单', content_object=item,
                                 object_repr=item)
        messages.add_message(request, messages.SUCCESS, '订单处理完成！')
        # return redirect('order_list_company_item', id=request.POST['back'], status=request.POST['status'])
        # return redirect('order_list_company_item', {'id':request.POST['back'], 'status':request.POST['status']})
        if request.POST['back'] or request.POST['status']:
            return redirect('/order_list_company?company='+request.POST['back']+ '&status='+request.POST['status'])
        else:
            return redirect('order_list_todo')
    else:
        return render(request, 'order_deal.html', {'item':item, 'back':request.GET['back'], 'status':request.GET['status']})


@login_required()
@permission_required('order.change_order',raise_exception=True)
def order_trouble(request,id):
    #问题单处理，用偷懒的方法，只显示最后一次评论，事实上确实最后一次评论对当前状态有意义
    if request.method == 'POST':
        item = get_object_or_404(Order, pk=id)
        item.status = '6'
        item.save()
        Ordercomment.objects.create(order=item, account=request.user, content=request.POST['trouble'])
        Operation.objects.create(account=request.user, action='3', description='标注问题订单', content_object=item,
                                 object_repr=item)
        messages.add_message(request, messages.ERROR, '订单已转成问题单！')
    if request.POST['back'] or request.POST['status']:
        return redirect('/order_list_company?company=' + request.POST['back'] + '&status=' + request.POST['status'])
    else:
        return redirect('order_list_todo')


@login_required()
@permission_required('order.change_order',raise_exception=True)
def order_change_delivery_code(request,id):
    # 订单处理后再次修改物流单号的情况
    item = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        item.delivery_code = request.POST['delivery_code']
        item.save()
        if request.POST['back'] or request.POST['status']:
            return redirect('/order_list_company?company='+request.POST['back']+ '&status='+request.POST['status'])
        else:
            return redirect('order_list_todo')
    else:
        return render(request, 'order_change_delivery_code.html', {'item': item, 'back':request.GET['back'], 'status':request.GET['status']})


@login_required()
def order_cancel(request,id):
    item = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        if item.status == '2':
            item.status = '7'
            item.save()
            Operation.objects.create(account=request.user, action='12', description='取消订单', content_object=item,
                                     object_repr=item)
            messages.add_message(request, messages.SUCCESS, '订单取消完成！')
        elif item.status == '3':
            stock_change(request, type='cancel', order_id=id)
            item.status = '7'
            item.save()
            Operation.objects.create(account=request.user, action='12', description='取消订单', content_object=item,
                                     object_repr=item)
            messages.add_message(request, messages.SUCCESS, '订单取消完成！')
        else:
            messages.add_message(request, messages.ERROR, '该订单无法取消！')

        if request.POST['back'] or request.POST['status']:
            return redirect('/order_list_company?company=' + request.POST['back'] + '&status=' + request.POST['status'])
        else:
            return redirect('order_list_todo')


# @login_required()
# @permission_required('order.change_order',raise_exception=True)
# def order_out(request,id):
#     #订单出库，已发货，库存从正常转为已出库，扣除运费，订单状态‘4’‘已出库’
#     # 取消订单出库的操作，转移库存移动到订单处理中，扣运费转移到订单完结中
#     item = get_object_or_404(Order, pk=id)
#     if request.method == 'POST':
#         item.final_delivery_fee = request.POST['final_delivery_fee']
#         item.status = '4'
#         stock_change(request, type='out', order_id=id)
#         company = item.company
#         Prepayrecord.objects.create(company=company, account=request.user, sum=-Decimal(item.final_delivery_fee), type=4,
#                                     instruction='订单%s的运费' % item.order_code, order=item)
#         company.prepayment -= Decimal(item.final_delivery_fee)
#         company.save()
#         item.save()
#         Operation.objects.create(account=request.user, action='3', description='订单出库', content_object=item,
#                                  object_repr=item)
#         messages.add_message(request, messages.SUCCESS, '订单出库完成！')
#         if request.POST['back'] or request.POST['status']:
#             return redirect('/order_list_company?company='+request.POST['back']+ '&status='+request.POST['status'])
#         else:
#             return redirect('order_list_todo')
#     else:
#         return render(request, 'order_out.html', {'item': item, 'back':request.GET['back'], 'status':request.GET['status']})


@login_required()
@permission_required('order.change_order',raise_exception=True)
def order_over(request,id):
    #订单完结，客户已收货，库存从已出库删除，订单状态‘5’‘已完成’
    #TODO 将扣运费转入此流程
    item = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        # 扣除运费钱最终确认运费
        item.final_delivery_fee = request.POST['final_delivery_fee']
        # 改变库存，将待出库数量清除
        item.status = '5'
        item.save()
        stock_change(request, type='over', order_id=id)
        # 扣除运费
        company = item.company
        Prepayrecord.objects.create(company=company, account=request.user, sum=-Decimal(item.final_delivery_fee), type=4,
                                    instruction='订单%s的运费' % item.order_code, order=item)
        company.prepayment -= Decimal(item.final_delivery_fee)
        company.save()
        Operation.objects.create(account=request.user, action='3', description='订单完结', content_object=item,
                                 object_repr=item)
        messages.add_message(request, messages.SUCCESS, '订单已完结！')
        if request.POST['back'] or request.POST['status']:
            return redirect('/order_list_company?company='+request.POST['back']+ '&status='+request.POST['status'])
        else:
            return redirect('order_list_todo')
    else:
        return render(request, 'order_out.html', {'item': item, 'back':request.GET['back'], 'status':request.GET['status']})


@login_required()
def reject_list(request):
    #退件列表
    content_type = ContentType.objects.get_for_model(Reject)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    if request.user.is_staff:
        search = request.GET.get('search')
        if search:
            data = Reject.objects.filter(
                Q(sales_record_number__icontains=search) | Q(reject_code__icontains=search) | Q(delivery_code__icontains=search)
            ).order_by('-id')
        else:
            data = Reject.objects.all().order_by('-id')
        select_company = SelectCompanyForm()
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'reject_list.html',
                      {'contacts': contacts, 'op': operate_record, 'select_company': select_company,'search': search,})
    else:
        search = request.GET.get('search')
        if search:
            data = Reject.objects.filter(company=request.user.company).filter(
                Q(sales_record_number__icontains=search) | Q(reject_code__icontains=search) | Q(delivery_code__icontains=search)
            ).order_by('-id')
        else:
            data = Reject.objects.filter(company=request.user.company).order_by('-id')
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'reject_list.html',{'contacts': contacts, 'op': operate_record,'search': search,})



@login_required()
def reject_list_company(request):
    content_type = ContentType.objects.get_for_model(Reject)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    if request.user.is_staff:
        company = request.GET['company']
        data = Reject.objects.filter(company=company).order_by('-id')
        select_company = SelectCompanyForm(initial={'company': company})
        back = company
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'reject_list.html', {'contacts': contacts, 'op': operate_record,
                                                    'select_company': select_company, 'back': back,
                                                    'selected_company_id': request.GET['company']})
    else:
        data = Reject.objects.filter(company=request.user.company).order_by('-id')
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'reject_list.html', {'contacts': contacts, 'op': operate_record,})



@login_required()
def reject_list_company_item(request,id):
    content_type = ContentType.objects.get_for_model(Reject)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    if request.user.is_staff:
        data = Reject.objects.filter(company=id).order_by('-id')
        select_company = SelectCompanyForm(initial={'company': id})
        back = id
    else:
        data = Reject.objects.filter(company=request.user.company).order_by('-id')
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'reject_list.html', {'contacts': contacts, 'op': operate_record,  'select_company': select_company, 'back':back})


@login_required()
@permission_required('order.add_reject', raise_exception=True)
def reject_create(request):
    # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])
    if request.method == 'GET':
        form = RejectForm(initial={'company':request.GET['back']})
        return render(request, 'reject_create.html', {'form': form,'sku_code_list':sku_belongs_to_company,'back': request.GET['back'],})
    else:
        new = RejectForm(request.POST)
        # 解析post，用的很笨的办法
        # result = []
        result = {}
        for n in range(len(request.POST)):
            index_s = "sku_code_" + str(n)
            index_a = "amount_" + str(n)
            if index_s in request.POST:
                result[request.POST[index_s]] = request.POST[index_a]
        if new.is_valid():
            log = new.save(commit=False)
            company = log.company
            log.reject_code = Reject.create_reject_code()
            # 对结果进行处理
            # 错误列表
            # 检查SKU是否正确(退单不检查数量，只检查是否输入了正确的SKU)
            errors = []
            for key, value in result.items():
                try:
                    sku = Sku.objects.get(code=key, company=company, status='1')
                except:
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                return render(request, 'reject_create.html', {
                    'form': new,
                    'data': change_type(result, company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                    'back': request.POST['back'],
                })
            else:
                # 保存退件单,这里涉及数据一致性的问题
                log = new.save()
                for key,value in result.items():
                    sku = Sku.objects.get(code=key, company=company, status='1')
                    Rejectcontain.objects.create(reject=log,sku=sku,amount=int(value))
                #创建时扣除退件检查费
                clf = Customerlevelfee.objects.get(level=company.level)
                Prepayrecord.objects.create(company=company, account=request.user, reject=log,
                                            sum=-Decimal(clf.reject_check_fee), type=6,
                                            instruction='退单%s的接收检查费' % log.reject_code)
                company.prepayment -= Decimal(clf.reject_check_fee)
                company.save()
                messages.add_message(request, messages.SUCCESS, '新退件创建成功！')
                Operation.objects.create(account=request.user, action='1', description='创建新退件', content_object=log,
                                         object_repr=log)
                if request.POST['back']:
                    return redirect('reject_list_company_item', id=int(request.POST['back']))
                else:
                    return redirect('reject_list')
        else:
            return render(request, 'reject_create.html', {'form': new,'data':change_type(result, request.POST['company']),
                    'id': request.POST['id'], 'back': request.POST['back'],
                    'sku_code_list': sku_belongs_to_company,})


@login_required()
@permission_required('order.change_reject', raise_exception=True)
def reject_edit(request,id):
    old = get_object_or_404(Reject, pk=id)
    # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(company=old.company, status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])
    # 获取运单SKU信息
    skus = Rejectcontain.objects.filter(reject=old)
    data = {}
    for item in skus:
        data[item.sku.code] = item.amount

    if request.method == 'POST':
        new = RejectForm(request.POST, instance=old)
        # 解析post，用的很笨的办法
        result = {}
        for n in range(len(request.POST)):
            index_s = "sku_code_" + str(n)
            index_a = "amount_" + str(n)
            if index_s in request.POST:
                result[request.POST[index_s]] = request.POST[index_a]

        if new.is_valid():
            # 对结果进行处理
            # 错误列表
            # 检查SKU是否正确、是否有足够的数量
            errors = []
            for key, value in result.items():
                try:
                    sku = Sku.objects.get(code=key, company=old.company, status='1')
                except:
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                return render(request, 'reject_edit.html', {
                    'form': new,
                    'data': change_type(result, old.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                    'back': request.POST['back'],
                })
            else:
                log = new.save()
                preds = Rejectcontain.objects.filter(reject=log)
                for p in preds:
                    p.delete()
                for key, value in result.items():
                    sku = Sku.objects.get(code=key, company=old.company, status='1')
                    Rejectcontain.objects.create(reject=old, sku=sku, amount=int(value))
                messages.add_message(request, messages.SUCCESS, '退件修改成功！')
                Operation.objects.create(account=request.user, action='3', description='修改退件单', content_object=log,
                                         object_repr=log)
                if request.POST['back']:
                    return redirect('reject_list_company_item', id=int(request.POST['back']))
                else:
                    return redirect('reject_list')
        else:
            return render(request, 'reject_edit.html', {'form': new, 'id': id, 'data':change_type(result,old.company),
                                                        'sku_code_list': sku_belongs_to_company,'back': request.POST['back'],})
    else:
        form = RejectForm(instance=old)
        return render(request, 'reject_edit.html',{'form': form, 'id': id, 'data':change_type(data,old.company),
                                                        'sku_code_list': sku_belongs_to_company,'back': request.GET['back'],})


@login_required()
@permission_required('order.delete_reject', raise_exception=True)
def reject_del(request,id):
    log = get_object_or_404(Reject,pk=id)
    Operation.objects.create(account=request.user, action='2', description='删除退件单', content_object=log,
                             object_repr=log)
    log.delete()
    messages.add_message(request, messages.SUCCESS, '退单删除成功！')
    if request.POST['back']:
        return redirect('reject_list_company_item', id=int(request.POST['back']))
    else:
        return redirect('reject_list')


@login_required()
@permission_required('order.change_reject', raise_exception=True)
def reject_over(request,id):
    log = get_object_or_404(Reject, pk=id)
    log.stock_time = log.count_reject_stock_time()
    log.stock_fee = log.count_reject_stock_fee()
    log.status = '2'
    log.save()
    Operation.objects.create(account=request.user, action='3', description='完结退件单', content_object=log,
                             object_repr=log)
    messages.add_message(request, messages.SUCCESS, '退单已完结！')
    if request.POST['back']:
        return redirect('reject_list_company_item', id=int(request.POST['back']))
    else:
        return redirect('reject_list')

@login_required()
def delivery_list(request):
    data = Delivery.objects.all()
    content_type = ContentType.objects.get_for_model(Delivery)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request, 'delivery_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['order.change_delivery','account.add_delivery'],raise_exception=True)
def delivery_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = DeliveryForm()
        else:
            old = get_object_or_404(Delivery,pk=id)
            form = DeliveryForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'delivery_edit.html', context)
    else:
        if id == 0:
            new = DeliveryForm(request.POST)
            mess = '新物流方案添加成功！'
            action_id = '1'
            des = '创建新物流方案'
        else:
            old = Delivery.objects.get(id=id)
            new = DeliveryForm(request.POST, instance=old)
            mess = '物流方案修改成功！'
            action_id = '3'
            des = '修改物流方案'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'delivery_edit.html', {'form': new,'id':id})
        return redirect('delivery_list')


@login_required()
@permission_required('account.delete_delivery',raise_exception=True)
def delivery_del(request,id):
    if request.method == 'POST':
        log = get_object_or_404(Delivery,pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除物流方案', content_object=log,
                                 object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '物流方案删除成功！')
        return redirect('delivery_list')

@login_required()
def delivery_query_list(request):
    # #queryset的数值转为list
    # data = Delivery.objects.filter(level=request.user.company.level).values_list()
    # #里面的每个记录都转为list
    # result = []
    # for item in data:
    #     item = item[:]
    #     result.append(item)
    # #利用numpy转换行列
    # import numpy as np
    # result = np.transpose(result)

    data = Delivery.objects.filter(level=request.user.company.level)
    return render(request, 'delivery_query_list.html', {'data':data})

@login_required()
def orderspecial_list(request):
    data = Orderspecial.objects.all()
    content_type = ContentType.objects.get_for_model(Orderspecial)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request, 'orderspecial_list.html', {'data': data,'op':operate_record})


@login_required()
@permission_required('order.add_orderspecial',raise_exception=True)
def orderspecial_create(request):
    if request.method == 'GET':
        form = OrderspecialForm()
        return render(request, 'orderspecial_create.html',{'form':form})
    else:
        form = OrderspecialForm(request.POST)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='1', description='添加特殊邮编', content_object=log,
                                     object_repr=log)
            messages.add_message(request, messages.SUCCESS, '特殊邮编添加成功！')
            return redirect('orderspecial_list')
        else:
            return render(request,'orderspecial_create.html',{'form':form})



@login_required()
@permission_required('order.change_orderspecial',raise_exception=True)
def orderspecial_edit(request, id):
    old = get_object_or_404(Orderspecial, pk=id)
    if request.method == 'GET':
        form = OrderspecialForm(instance=old)
        return render(request,'orderspecial_edit.html',{'form':form,'id':id})
    else:
        form = OrderspecialForm(request.POST, instance=old)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='3', description='修改特殊邮编', content_object=log,
                                     object_repr=log)
            messages.add_message(request, messages.SUCCESS, '特殊邮编编辑成功！')
            return redirect('orderspecial_list')
        else:
            return render(request, 'orderspecial_edit.html', {'form': form,'id':id})


@login_required()
@permission_required('order.delete_orderspecial',raise_exception=True)
def orderspecial_del(request,id):
    log = get_object_or_404(Orderspecial,pk=id)
    Operation.objects.create(account=request.user, action='2', description='删除特殊邮编', content_object=log,
                             object_repr=log)
    log.delete()
    messages.add_message(request, messages.SUCCESS, '特殊邮编删除成功！')
    return redirect('orderspecial_list')



