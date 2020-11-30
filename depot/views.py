from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.forms.models import modelformset_factory,inlineformset_factory
from django.shortcuts import get_object_or_404,redirect,HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
import xlwt
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


from account.models import Operation,Prepayrecord
from .models import *
from .forms import *
from order.models import Order, Ordercontain



# Create your views here.


@login_required()
def depot_list(request):
    data = Depot.objects.all()
    content_type = ContentType.objects.get_for_model(Depot)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'depot_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['depot.change_depot','depot.add_depot'],raise_exception=True)
def depot_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = DepotForm()
        else:
            old = get_object_or_404(Depot,pk=id)
            form = DepotForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'depot_edit.html', context)
    else:
        if id == 0:
            new = DepotForm(request.POST)
            mess = '新仓库添加成功！'
            action_id = '1'
            des = '创建新仓库'
        else:
            old = get_object_or_404(Depot,pk=id)
            new = DepotForm(request.POST, instance=old)
            mess = '仓库信息修改成功！'
            action_id = '3'
            des = '修改仓库信息'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'depot_edit.html', {'form': new,'id':id})
        return redirect('depot_list')


@login_required()
@permission_required('depot.delete_depot', raise_exception=True)
def depot_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Depot, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除仓库', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '仓库删除成功！')
        return redirect('depot_list')


@login_required()
def unit_list(request):
    data = Unit.objects.all()
    content_type = ContentType.objects.get_for_model(Unit)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'unit_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['depot.change_unit','depot.add_unit'],raise_exception=True)
def unit_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = UnitForm()
        else:
            old = get_object_or_404(Unit,pk=id)
            form = UnitForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'unit_edit.html', context)
    else:
        if id == 0:
            new = UnitForm(request.POST)
            mess = '新库位添加成功！'
            action_id = '1'
            des = '创建新库位'
        else:
            old = get_object_or_404(Unit,pk=id)
            new = UnitForm(request.POST, instance=old)
            mess = '库位信息修改成功！'
            action_id = '3'
            des = '修改库位信息'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'unit_edit.html', {'form': new,'id':id})
        return redirect('unit_list')


@login_required()
@permission_required('depot.delete_unit', raise_exception=True)
def unit_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Unit, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除库位', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '库位删除成功！')
        return redirect('unit_list')


@login_required()
@permission_required('depot.add_unit', raise_exception=True)
def unit_init(request):
    #库位初始化
    form = UnitInitForm()
    if request.method == 'POST':
        sum = Unit.objects.filter(depot=request.POST['depot']).count()
        if sum > 0:
            messages.add_message(request, messages.ERROR, '无法对该仓库进行初始化，只能对未设置任何库位的仓库进行初始化。')
            return render(request, 'unit_init.html', {'form': form})
        else:
            depot = Depot.objects.get(id = request.POST['depot'])
            for first in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']:
                for second in range(1,6):
                    for third in ['a','b','c','d','e']:
                        name = first + str(second) + third
                        Unit.objects.create(depot=depot, name=name)
            data = Unit.objects.all()
            return render(request, 'unit_list.html', {'data': data,})
    else:
        return render(request, 'unit_init.html',{'form':form})


@login_required()
def skutype_list(request):
    data = Skutype.objects.all()
    content_type = ContentType.objects.get_for_model(Skutype)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'skutype_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['depot.change_skutype','depot.add_skutype'],raise_exception=True)
def skutype_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = SkutypeForm()
        else:
            old = get_object_or_404(Skutype,pk=id)
            form = SkutypeForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'skutype_edit.html', context)
    else:
        if id == 0:
            new = SkutypeForm(request.POST)
            mess = '新SKU类别添加成功！'
            action_id = '1'
            des = '创建新SKU类别'
        else:
            old = get_object_or_404(Skutype,pk=id)
            new = SkutypeForm(request.POST, instance=old)
            mess = 'SKU类别修改成功！'
            action_id = '3'
            des = '修改SKU类别'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'skutype_edit.html', {'form': new,'id':id})
        return redirect('skutype_list')


@login_required()
@permission_required('depot.delete_skutype', raise_exception=True)
def skutype_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Skutype, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除SKU类别', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, 'SKU类别删除成功！')
        return redirect('skutype_list')


@login_required()
def skutypefee_list(request):
    data = Skutypefee.objects.all()
    content_type = ContentType.objects.get_for_model(Skutypefee)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'skutypefee_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['depot.change_skutypefee','depot.add_skutypefee'],raise_exception=True)
def skutypefee_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = SkutypefeeForm()
        else:
            old = get_object_or_404(Skutypefee,pk=id)
            form = SkutypefeeForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'skutypefee_edit.html', context)
    else:
        if id == 0:
            new = SkutypefeeForm(request.POST)
            mess = '新SKU类别费用添加成功！'
            action_id = '1'
            des = '创建新SKU类别费用'
        else:
            old = get_object_or_404(Skutypefee,pk=id)
            new = SkutypefeeForm(request.POST, instance=old)
            mess = 'SKU类别费用修改成功！'
            action_id = '3'
            des = '修改SKU类别费用'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'skutypefee_edit.html', {'form': new,'id':id})
        return redirect('skutypefee_list')


@login_required()
@permission_required('depot.delete_skutypefee', raise_exception=True)
def skutypefee_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Skutypefee, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除SKU类别费用', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, 'SKU类别费用删除成功！')
        return redirect('skutypefee_list')


@login_required()
def customerlevelfee_list(request):
    data = Customerlevelfee.objects.all()
    content_type = ContentType.objects.get_for_model(Customerlevelfee)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'customerlevelfee_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['depot.change_customerlevelfee','depot.add_customerlevelfee'],raise_exception=True)
def customerlevelfee_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = CustomerlevelfeeForm()
        else:
            old = get_object_or_404(Customerlevelfee,pk=id)
            form = CustomerlevelfeeForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'customerlevelfee_edit.html', context)
    else:
        if id == 0:
            new = CustomerlevelfeeForm(request.POST)
            mess = '新客户等级费用添加成功！'
            action_id = '1'
            des = '创建新客户等级费用'
        else:
            old = get_object_or_404(Customerlevelfee,pk=id)
            new = CustomerlevelfeeForm(request.POST, instance=old)
            mess = '客户等级费用修改成功！'
            action_id = '3'
            des = '修改客户等级费用'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'customerlevelfee_edit.html', {'form': new,'id':id})
        return redirect('customerlevelfee_list')


@login_required()
@permission_required('depot.delete_customerlevelfee', raise_exception=True)
def customerlevelfee_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Customerlevelfee, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除客户等级类别费用', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '客户等级费用删除成功！')
        return redirect('customerlevelfee_list')


@login_required()
def sku_list(request):
    content_type = ContentType.objects.get_for_model(Sku)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    if request.user.is_staff:
        search = request.GET.get('search')
        if search:
            data = Sku.objects.filter(
                Q(name__icontains=search) | Q(name_en__icontains=search) | Q(leo_code__icontains=search) | Q(code__icontains=search)
            ).order_by('-id')
        else:
            data = Sku.objects.all().order_by('-id')

        select_company = SelectCompanyForm()
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts': contacts, 'op': operate_record,
                                                 'select_company':select_company, 'search':search})
    else:
        search = request.GET.get('search')
        if search:
            data = Sku.objects.filter(company=request.user.company).filter(
                Q(name__icontains=search) | Q(name_en__icontains=search) | Q(leo_code__icontains=search) | Q(code__icontains=search)
            ).order_by('-id')
        else:
            data = Sku.objects.filter(company=request.user.company).order_by('-id')

        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts':contacts,'op':operate_record, 'search':search})


@login_required()
def sku_list_company(request):
    # 根据用户选择的公司，显示该公司的所有SKU，因为用form传参，所以不需参数
    content_type = ContentType.objects.get_for_model(Sku)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by(
        '-action_time')[:10]
    if request.user.is_staff:
        company = request.GET['company']
        data = Sku.objects.filter(company=company).order_by('-id')
        select_company = SelectCompanyForm(initial={'company':company})
        back = company
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts': contacts, 'op': operate_record,
                                                 'select_company': select_company, 'back':back,
                                                 'selected_company_id': request.GET['company']})
    else:
        data = Sku.objects.filter(company=request.user.company).order_by('-id')
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts': contacts, 'op': operate_record})


@login_required()
def sku_list_company_item(request,id):
    # 在指定公司SKU页面下，进行操作后返回公司SKU页面，因为没有form，所以用url传参
    content_type = ContentType.objects.get_for_model(Sku)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by(
        '-action_time')[:10]
    if request.user.is_staff:
        data = Sku.objects.filter(company_id=id).order_by('-id')
        select_company = SelectCompanyForm(initial={'company':id})
        back = id
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts': contacts, 'op': operate_record,
                                                 'select_company': select_company, 'back':back})
    else:
        data = Sku.objects.filter(company=request.user.company).order_by('-id')
        paginator = Paginator(data, 25)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, 'sku_list.html', {'contacts': contacts, 'op': operate_record})


@login_required()
@permission_required('depot.add_sku',raise_exception=True)
def sku_create(request):
    if request.method == 'GET':
        form = SkuCreateForm(initial={'company': request.user.company,'leo_code':Sku.create_leo_code() })
        return render(request, 'sku_create.html', {'form':form})
    if request.method == 'POST':
        new = SkuCreateForm(request.POST, request.FILES)
        if new.is_valid():
            log = new.save()
            log.save()
            messages.add_message(request, messages.SUCCESS, '新SKU添加成功！')
            Operation.objects.create(account=request.user, action='1', description='创建新SKU', content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'sku_create.html', {'form': new, 'id': id})
        return redirect('sku_list')


@login_required()
@permission_required('depot.change_sku',raise_exception=True)
def sku_edit(request,id):
    if request.method == 'GET':
        old = get_object_or_404(Sku,pk=id)
        form = SkuEditForm(instance=old)
        context = {'form':form, 'id':id, 'back':request.GET['back']}
        return render(request, 'sku_edit.html', context)
    else:
        old = get_object_or_404(Sku,pk=id)
        new = SkuEditForm(request.POST, request.FILES,instance=old)
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, 'SKU修改成功！')
            Operation.objects.create(account=request.user, action='3', description='修改SKU', content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'sku_edit.html', {'form': new,'id':id})
        if request.POST['back']:
            return redirect('sku_list_company_item',id=int(request.POST['back']))
        else:
            return redirect('sku_list')
        # HttpResponseRedirect会定向到当前url下面
        # return HttpResponseRedirect(request.POST['back'])


@login_required()
@permission_required('depot.delete_sku', raise_exception=True)
def sku_del(request, id):
    # 删除SKU前必须校验是否还有库存，有库存要提示不能删除
    if request.method == 'POST':
        log = get_object_or_404(Sku, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除SKU', content_object=log,
                                                              object_repr=log)
        log.delete()
        # 这里做了删除前的判断，客户说不需要，直接删除对应的库存数量
        # if not log.is_exist():
        #     Operation.objects.create(account=request.user, action='2', description='删除SKU', content_object=log,
        #                              object_repr=log)
        #     log.delete()
        # else:
        #     messages.add_message(request, messages.SUCCESS, '该SKU还有库存，不能删除！')
        #     return redirect('sku_list')
        messages.add_message(request, messages.SUCCESS, 'SKU删除成功！')
        if request.POST['back']:
            return redirect('sku_list_company_item',id=int(request.POST['back']))
        else:
            return redirect('sku_list')


def download_skus(request):
    # TODO sku的多仓库情况未处理
    # 导出所有SKU，客户导出自己的，仓库导出全部
    if request.user.is_staff:
        data = Sku.objects.filter(status='1')
    else:
        data = Sku.objects.filter(company=request.user.company, status='1')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=sku_list.xls'
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    # 表头，订单导出时可以去掉，去掉后记得改后面的行号
    row0 = ['序号', '客户SKU编号', '中文名', '英文名', '雷欧编码', '海关申报代码', '申报价值', '重量', '体积',
            '长度', '宽度', '高度', '商品品类', '正常数量','待入库数量','待出库数量','缺货数量','冻结数量','其他数量']
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    # 从第一行开始依次写入数据
    # 包含的SKU要合并在一个单元各内
    row = 1
    for i in range(0, len(data)):
        sheet.write(row, 0, i+1)
        sheet.write(row, 1, data[i].code)
        sheet.write(row, 2, data[i].name)
        sheet.write(row, 3, data[i].name_en)
        sheet.write(row, 4, data[i].leo_code)
        sheet.write(row, 5, data[i].declare_code)
        sheet.write(row, 6, data[i].price)
        sheet.write(row, 7, data[i].weight)
        sheet.write(row, 8, data[i].height)
        sheet.write(row, 9, data[i].length)
        sheet.write(row, 10, data[i].width)
        sheet.write(row, 11, data[i].height)
        sheet.write(row, 12, data[i].category)
        nums = data[i].count_set.last()
        if nums:
            sheet.write(row, 13, nums.normal)
            sheet.write(row, 14, nums.preparing_in)
            sheet.write(row, 15, nums.preparing_out)
            sheet.write(row, 16, nums.short)
            sheet.write(row, 17, nums.freeze)
            sheet.write(row, 18, nums.other)
        row = row + 1
    workbook.save(response)
    return response


@login_required()
def sku_examine_list(request):
    data = Sku.objects.filter(status='0').order_by('-id')
    operate_record = Operation.objects.filter(action='5').order_by('-action_time')[:10]
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'sku_examine_list.html', {'contacts': contacts, 'op': operate_record})


@login_required()
@permission_required('depot.change_sku', raise_exception=True)
def sku_examine_edit(request,id):
    if request.method == 'GET':
        old = get_object_or_404(Sku,pk=id)
        form = SkuExamineForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'sku_examine_edit.html', context)
    else:
        old = get_object_or_404(Sku,pk=id)
        new = SkuExamineForm(request.POST, request.FILES,instance=old)
        if new.is_valid():
            log = new.save()
            depots = Depot.objects.all()
            for d in depots:
                try:
                    Count.objects.get(sku=log,depot=d)
                except Count.DoesNotExist:
                    Count.objects.create(sku=log, depot=d)
            messages.add_message(request, messages.SUCCESS, 'SKU审核完成')
            Operation.objects.create(account=request.user, action='5', description='仓库修改SKU信息', content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'sku_examine_edit.html', {'form': new,'id':id})
        return redirect('sku_examine_list')


@login_required()
@permission_required('depot.change_sku', raise_exception=True)
def sku_check_again(request,sku_id,trans_id):
    #从运单审核页面进入的sku修改
    #先获取库位信息
    old = Sku.objects.get(id=sku_id)
    trans = get_object_or_404(Transorder, pk=trans_id)
    sku_count = get_object_or_404(Count, sku=old, depot=trans.depot)

    if request.method == 'POST':
        form = SkuExamineForm(request.POST, request.FILES, instance=old)
        unit_form = SkuUnitForm(request.POST,instance=sku_count)
        unit_form.fields['unit'].queryset = Unit.objects.filter(depot=trans.depot)
        if form.is_valid() and unit_form.is_valid():
            log = form.save()
            unit_form.save()
            messages.add_message(request, messages.SUCCESS, 'SKU修改成功！')
            Operation.objects.create(account=request.user, action='5', description='仓库修改SKU信息', content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'sku_check_again.html', {
                'form': form,
                'sku_id': sku_id,
                'trans_id': trans_id,
                'unit_form': unit_form,
            })
        ts = Transorder.objects.get(id=trans_id)
        PredictionFormSet = modelformset_factory(Prediction,fields=('amount', 'check'),
                                                 widgets={
                                                     'amount': forms.TextInput(attrs={'readonly': 'readonly'}),
                                                 },
                                                 extra=0)
        prediction_list = Prediction.objects.filter(transorder=ts).order_by('id')
        formset = PredictionFormSet(queryset=prediction_list)
        return render(request, 'transorder_check_edit.html', {
            'data': ts,
            'formset': formset,
            'pre_data': prediction_list,
            'id': trans_id,
        })
    else:
        form = SkuExamineForm(instance=old,)
        unit_form = SkuUnitForm(instance=sku_count)
        unit_form.fields['unit'].queryset = Unit.objects.filter(depot=trans.depot)
        return render(request, 'sku_check_again.html', {
            'form': form,
            'sku_id': sku_id,
            'trans_id': trans_id,
            'unit_form':unit_form,
        })


@login_required()
def transorder_list(request):
    data = Transorder.objects.filter(company=request.user.company).order_by('-id')
    content_type = ContentType.objects.get_for_model(Transorder)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'transorder_list.html', {'contacts': contacts, 'op': operate_record})


@login_required()
@permission_required('depot.add_transorder', raise_exception=True)
def transorder_create(request):

    # 判断预付费是否充足
    if request.user.company.prepayment < 100:
        return redirect('backend:index')

    # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(company=request.user.company, status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])

    if request.method == 'GET':
        form = TransorderForm(initial={'company': request.user.company, })
        return render(request, 'transorder_create.html', {'form': form,'sku_code_list':sku_belongs_to_company})
    if request.method == 'POST':
        new = TransorderForm(request.POST)
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
            for key,value in result.items():
                try:
                    sku = Sku.objects.get(code=key, company=request.user.company,status='1')
                    # sum = Count.objects.get(sku=sku)
                    # if sum.normal < int(value):
                    #     error = "SKU:" + key + "数量不足，请重新检查"
                    #     errors.append(error)
                except :
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                return render(request, 'transorder_create.html', {
                    'form': new,
                     'data':change_type(result,request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                })
            else:
                log = new.save()
                for key,value in result.items():
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    Prediction.objects.create(transorder=log,sku=sku,amount=int(value))
                messages.add_message(request, messages.SUCCESS, '新到货预报创建成功！')
                Operation.objects.create(account=request.user, action='1', description='创建新到货预报', content_object=log,
                                         object_repr=log)
                return redirect('transorder_list')
        else:
            return render(request, 'transorder_create.html', {
                    'form': new,
                    'data':change_type(result,request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,})

#         t = Transorder.objects.get(id=request.GET['id'])
#         data = Prediction.objects.filter(transorder=t)
#         sku_code_list = Sku.objects.filter(company=request.user.company,status='1')
#         return render(request, 'transorder_sum.html', {'data':data,'id':request.GET['id'],'sku_code_list':sku_code_list})


def change_type(sku_result, company):
    # 转换结果，包含sku名称及库存数量
    data = []
    for key,value in sku_result.items():
        item = {}
        try:
            sku = Sku.objects.get(code=key, company=company)
            item['sku_code'] = key
            item['sku_name'] = sku.name
            item['quantity'] = sku.count_set.last().normal
            item['amount'] = value
            data.append(item)
        except:
            item['sku_code'] = key
            item['amount'] = value
            data.append(item)
    return data


@login_required()
@permission_required('depot.change_transorder', raise_exception=True)
def transorder_edit(request,id):
    old = get_object_or_404(Transorder, pk=id)
    # 获取输入框SKU代码提示
    sku_code_list = Sku.objects.filter(company=request.user.company, status='1').values('code')
    sku_belongs_to_company = []
    for item in sku_code_list:
        sku_belongs_to_company.append(item['code'])
    # 获取运单SKU信息
    skus = Prediction.objects.filter(transorder=old)
    data = {}
    for item in skus:
        data[item.sku.code] = item.amount

    if request.method == 'POST':
        new = TransorderForm(request.POST, instance=old)
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
                    # sum = Count.objects.get(sku=sku)
                    # if sum.normal < int(value):
                    #     error = "SKU:" + key + "数量不足，请重新检查"
                    #     errors.append(error)
                except:
                    error = "SKU:" + key + "错误，只有通过审核的SKU才能添加到运单之中，请检查您的输入。"
                    errors.append(error)
            # 有错误则返回处理，没错误则保存添加
            if errors:
                return render(request, 'transorder_edit.html', {
                    'form': new,
                    'data':change_type(result,request.user.company),
                    'id': request.POST['id'],
                    'sku_code_list': sku_belongs_to_company,
                    'errors': errors,
                })
            else:
                log = new.save()
                preds = Prediction.objects.filter(transorder=log)
                for p in preds:
                    p.delete()
                for key, value in result.items():
                    sku = Sku.objects.get(code=key, company=request.user.company, status='1')
                    Prediction.objects.create(transorder=log, sku=sku, amount=int(value))
                messages.add_message(request, messages.SUCCESS, '到货预报修改成功！')
                Operation.objects.create(account=request.user, action='3', description='修改到货预报运单', content_object=log,
                                         object_repr=log)
                return redirect('transorder_list')
        else:
            return render(request, 'transorder_edit.html', {'form': new, 'id': id,  'data':change_type(result,request.user.company),
                    'sku_code_list': sku_belongs_to_company,})

    else:
        form = TransorderForm(instance=old)
        return render(request, 'transorder_edit.html', {'form': form, 'id': id, 'data':change_type(data,request.user.company),
                                                        'sku_code_list': sku_belongs_to_company,})


@login_required()
@permission_required('depot.delete_transorder', raise_exception=True)
def transorder_del(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Transorder, pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除预报运单', content_object=log,
                                     object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '预报运单删除成功！')
        return redirect('transorder_list')


def get_sku_status(request):
    sku_code = request.GET['sku_code']
    company_id = request.GET['company_id']
    callback= request.GET['callback']
    data = {}
    try:
        sku = Sku.objects.get(code=sku_code, company_id=company_id)
        data['name'] = sku.name
        data['quantity'] = sku.count_set.last().normal
    except:
        data['name'] = '不存在此SKU'
        data['quantity'] = 0
    result=callback+"("+json.dumps(data)+")"
    return HttpResponse(result)
    # return HttpResponse(json.dumps(data),content_type="application/json")


@login_required()
def transorder_submit(request,id):
    transorder = get_object_or_404(Transorder, pk=id)
    transorder.status_trans = '2'
    stock_change(request,'prediction',id)
    transorder.save()
    #将审核数量的默认值设为预报数量
    for item in transorder.prediction_set.all():
        item.check = item.amount
        item.save()
    messages.add_message(request, messages.SUCCESS, '运单提交成功！')
    Operation.objects.create(account=request.user, action='6', description='提交到货预报运单', content_object=transorder,
                             object_repr=transorder)
    return redirect('transorder_list')


#库存变更函数，共有几种变更方法：
#1.到货预报：运单数量->待入库
#2.入库核对：待入库->正常(分配库位)
#3.订单处理：正常->待出库
#4.订单完成：待出库->出库完成
#5.管理员手动修改
#TODO sku目前和unit绑定 需要解决
@login_required()
def stock_change(request,type,order_id):
    if type == 'prediction':
        # 1.到货预报：运单数量->待入库
        in_list = Prediction.objects.filter(transorder_id=order_id)
        for item in in_list:
            try:
                count = Count.objects.get(sku = item.sku, depot=item.transorder.depot)
                count.preparing_in = count.preparing_in + item.amount
                count.save()
                instruction = '到货预报' + item.transorder.transport_code + '提交，SKU：' + item.sku.leo_code + '待入库数量变化：' + str(item.amount)
                Stockchange.objects.create(sku=item.sku, depot=item.transorder.depot, change_type='3', quantity=item.amount,
                                           company=item.sku.company, operate_style='1', instruction=instruction)
            except Count.DoesNotExist:
                Count.objects.create(sku=item.sku, depot=item.transorder.depot, preparing_in=item.amount)
    elif type == 'in':
        #TODO 如果后面的逻辑出错，可是前面的模型已经保存的话，怎么办
        #入库逻辑流程
        #变更运单状态为4.完结
        trans = get_object_or_404(Transorder,pk=order_id)
        #依次将预报运单中的SKU进行入库、并结算入仓费
        #结算费用
        #根据sku.skutype,transorder.company,company.level,company.prepayment,prepayrecord
        company = trans.company
        level = trans.company.level
        total = 0
        in_list = Prediction.objects.filter(transorder=trans)
        for item in in_list:
            try:
                #入库数量处理
                count = Count.objects.get(sku=item.sku,depot=trans.depot)
                count.preparing_in = count.preparing_in - item.amount
                count.normal = count.normal + item.check
                count.save()
                instruction = '到货预报' + trans.transport_code + '入库，SKU：' + item.sku.leo_code + '正常数量变化：' + str(item.check)
                instruction += ' 到货预报' + trans.transport_code + '入库，SKU：' + item.sku.leo_code + '待入库数量变化：' + str(-item.amount)
                Stockchange.objects.create(sku=item.sku,depot=trans.depot,change_type='1',quantity=item.check,
                                           company=company,operate_style='1',instruction=instruction)
            except Count.DoesNotExist:
                Count.objects.create(sku=item.sku, depot=item.transorder.depot, normal=item.check)
            #费用计算
            try:
                item_fee = Skutypefee.objects.get(skutype=item.sku.skutype,level=level)
                unit_price = item_fee.in_fee
            except Skutypefee.DoesNotExist:
                unit_price = 0
            total += unit_price * item.check
        #修改客户预存款
        company.prepayment = company.prepayment - total
        company.save()
        #变更运单状态
        trans.status_trans = '4'
        trans.save()
        Prepayrecord.objects.create(company=company, account=request.user, sum=-total, type=2, transorder=trans,
                                    instruction='到货预报%s的入仓费' % trans.transport_code)
        Operation.objects.create(account=request.user, action='8', description='运单入库', content_object=trans,
                                 object_repr=trans)

    elif type == 'out':
        #出库逻辑流程
        order = get_object_or_404(Order, pk=order_id)
        out_list = order.ordercontain_set.all()
        for item in out_list:
            # TODO 多仓库的情况，order中现在没有depot属性
            # count = Count.objects.get(sku=item.sku,depot=order.depot)
            count = Count.objects.get(sku_id=item.sku_id)
            count.normal = count.normal - item.amount
            count.preparing_out = count.preparing_out + item.amount
            count.save()
            instruction = '订单' + order.order_code + '出库，SKU：' + item.sku.leo_code + '正常数量变化：' + str(-item.amount)
            instruction += ' 订单' + order.order_code + '出库，SKU：' + item.sku.leo_code + '待出库数量变化：' + str(item.amount)
            Stockchange.objects.create(sku=item.sku, depot=order.depot, change_type='2', quantity=item.amount,
                                       company=order.company, operate_style='1')
            Operation.objects.create(account=request.user, action='9', description='订单出库', content_object=order,
                                     object_repr=order)
    elif type == 'over':
        #订单完结的逻辑
        # TODO 多仓库的情况，order中现在没有depot属性
        order = get_object_or_404(Order, pk=order_id)
        out_list = order.ordercontain_set.all()
        for item in out_list:
            count = Count.objects.get(sku=item.sku)
            count.preparing_out = count.preparing_out - item.amount
            count.save()
            instruction = '订单' + order.order_code + '收货，SKU：' + item.sku.leo_code + '待出库数量变化：' + str(-item.amount)
            Stockchange.objects.create(sku=item.sku, depot=order.depot, change_type='4', quantity=item.amount,
                                       company=order.company, operate_style='1',instruction=instruction)
            Operation.objects.create(account=request.user, action='11', description='订单完结', content_object=order,
                                     object_repr=order)
    elif type == 'cancel':
        #订单取消的逻辑
        # 将待出库库存转回正常库存
        order = get_object_or_404(Order, pk=order_id)
        out_list = order.ordercontain_set.all()
        for item in out_list:
            # TODO 多仓库的情况，order中现在没有depot属性
            # count = Count.objects.get(sku=item.sku,depot=order.depot)
            count = Count.objects.get(sku_id=item.sku_id)
            count.normal = count.normal + item.amount
            count.preparing_out = count.preparing_out - item.amount
            count.save()
            instruction = '订单' + order.order_code + '取消，SKU：' + item.sku.leo_code + '正常数量变化：' + str(item.amount)
            instruction += ' 订单' + order.order_code + '取消，SKU：' + item.sku.leo_code + '待出库数量变化：' + str(-item.amount)
            Stockchange.objects.create(sku=item.sku, depot=order.depot, change_type='6', quantity=item.amount,
                                       company=order.company, operate_style='1')
            Operation.objects.create(account=request.user, action='12', description='取消订单', content_object=order,
                                     object_repr=order)
    else:
        pass


# 到货审核列表
@login_required()
def transorder_check_list(request):
    data = Transorder.objects.exclude(status_trans='1').order_by('-id')
    operate_record = Operation.objects.filter(action='7').order_by('-action_time')[:10]
    select_company = SelectCompanyForm()
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'transorder_check_list.html', {'contacts': contacts,'op':operate_record,'select_company':select_company})


@login_required()
def transorder_list_company(request):
    # 根据用户选择的公司，显示该公司的所有运单，因为用form传参，所以不需参数
    content_type = ContentType.objects.get_for_model(Transorder)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by(
        '-action_time')[:10]
    company = request.GET['company']
    data = Transorder.objects.filter(company=company).exclude(status_trans='1').order_by('-id')
    select_company = SelectCompanyForm(initial={'company':company})
    back = company
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'transorder_check_list.html', {'contacts': contacts, 'op': operate_record,
                                             'select_company': select_company, 'back':back, 'selected_company_id': request.GET['company']})


@login_required()
def transorder_list_company_item(request,id):
    # 在指定公司运单页面下，进行操作后返回公司运单页面，因为没有form，所以用url传参
    content_type = ContentType.objects.get_for_model(Transorder)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by(
        '-action_time')[:10]
    data = Transorder.objects.filter(company_id=id).exclude(status_trans='1').order_by('-id')
    select_company = SelectCompanyForm(initial={'company':id})
    back = id
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'transorder_check_list.html', {'contacts': contacts, 'op': operate_record,
                                             'select_company': select_company, 'back':back})


#到货审核完结
@login_required()
@permission_required('depot.change_transorder', raise_exception=True)
def transorder_close(request,id):
    stock_change(request,'in',id)
    if request.POST['back']:
        return redirect('transorder_list_company_item', id=int(request.POST['back']))
    else:
        return redirect('transorder_check_list')


#到货审核操作页面
@login_required()
@permission_required('depot.change_transorder', raise_exception=True)
def transorder_check_edit(request,id):
    PredictionFormSet = modelformset_factory(Prediction,fields=('amount', 'check'),
                                             widgets={
                                                 'amount': forms.TextInput(attrs={'readonly': 'readonly'}),
                                             },
                                             extra=0)
    if request.method == 'GET':
        # 订单核对页面，显示订单信息及包含SKU的数量和其他信息
        ts = get_object_or_404(Transorder,pk=id)
        prediction_list = Prediction.objects.filter(transorder=ts).order_by('id')
        formset = PredictionFormSet(queryset=prediction_list)
        return render(request, 'transorder_check_edit.html', {
            'data': ts,
            'formset': formset,
            'pre_data': prediction_list,
            'id': id,
            'back': request.GET['back'],
        })
    else:
        # 核对订单，完成入库
        formset = PredictionFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            ts = get_object_or_404(Transorder,pk=id)
            ts.check = request.POST['check']
            ts.status_trans = '3'
            ts.save()
            messages.add_message(request, messages.SUCCESS, '到货预报核对完成！')
            Operation.objects.create(account=request.user, action='7', description='核对到货预报', content_object=ts,
                                     object_repr=ts)
            if request.POST['back']:
                return redirect('transorder_list_company_item', id=int(request.POST['back']))
            else:
                return redirect('transorder_check_list')
        else:
            ts = get_object_or_404(Transorder, pk=id)
            prediction_list = Prediction.objects.filter(transorder=ts).order_by('id')
            return render(request, 'transorder_check_edit.html', {
                'data': ts,
                'formset': formset,
                'pre_data': prediction_list,
                'id': id,
                'back': request.POST['back'],
            })


@login_required()
def transorder_look_over(request,id):
#已经核对完成的订单，显示订单信息，只能查看不能编辑
    ts = get_object_or_404(Transorder,pk=id)
    prediction_list = Prediction.objects.filter(transorder=ts).order_by('id')
    return render(request, 'transorder_look_over.html', {'data': ts,'pre_data': prediction_list,'back':request.GET['back']})


@login_required()
@permission_required('depot.change_count', raise_exception=True)
def sku_count_edit(request,id):
    #TODO 这里的问题，如果是手动修改的话，怎么计入stockchange表
    #TODO 详细比较每一个数据，出库、入库记录一定得计入变动记录
    #TODO 这个表最好记录清楚的变动记录
    #TODO count表的str和prep要为这里服务
    count = get_object_or_404(Count, pk=id)
    old_data = '原数据为：'+'正常：'+str(count.normal)+'待入库：'+str(count.preparing_in)+'待出库：'+\
               str(count.preparing_out)+'冻结：'+str(count.freeze)+'缺货：'+str(count.short)+'其他：'+str(count.other)
    if request.method == 'POST':
        form = CountForm(request.POST, instance=count)
        if form.is_valid():
            count = form.save()
            new_data = '新数据为：'+'正常：'+str(count.normal)+'待入库：'+str(count.preparing_in)+'待出库：'+\
               str(count.preparing_out)+'冻结：'+str(count.freeze)+'缺货：'+str(count.short)+'其他：'+str(count.other)
            instruction = old_data + ' ' + new_data
            Stockchange.objects.create(sku=count.sku, depot=count.depot, change_type='5', quantity=0,
                                       company=count.sku.company, operate_style='2', instruction=instruction)
            Operation.objects.create(account=request.user, action='10', description='仓库管理员手动编辑SKU数量', content_object=count,
                                     object_repr=count)

            if request.POST['back']:
                return redirect('sku_list_company_item', id=int(request.POST['back']))
            else:
                return redirect('sku_list')
        else:
            return render(request, 'sku_count_edit.html', {'form': form,'id':id})
    else:
        form = CountForm(instance=count)
        return render(request, 'sku_count_edit.html', {'form':form,'id':id,'back':request.GET['back']})


@login_required()
def storagefee_list(request):
    data = Storagefee.objects.all()
    content_type = ContentType.objects.get_for_model(Storagefee)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by(
        '-action_time')[:10]
    return render(request,'storagefee_list.html',{'data':data, 'op':operate_record})


@login_required()
@permission_required('depot.add_storagefee', raise_exception=True)
def storagefee_create(request):
    if request.method == 'GET':
        form = StoragefeeForm()
        return render(request,'storagefee_create.html',{'form':form})
    else:
        form = StoragefeeForm(request.POST)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='1', description='创建仓租费用方案',
                                     content_object=log,object_repr=log)
            return redirect('storagefee_list')
        else:
            return render(request, 'storagefee_create.html', {'form': form})

@login_required()
@permission_required('depot.change_storagefee', raise_exception=True)
def storagefee_edit(request,id):
    old = get_object_or_404(Storagefee,pk=id)
    if request.method == 'GET':
        form = StoragefeeForm(instance=old)
        return render(request, 'storagefee_edit.html',{'form':form,'id':id})
    else:
        form = StoragefeeForm(request.POST, instance=old)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='3', description='修改仓租费用方案',
                                     content_object=log, object_repr=log)
            return redirect('storagefee_list')
        else:
            return render(request, 'storagefee_edit.html', {'form': form,'id':id})


@login_required()
@permission_required('depot.delete_storagefee', raise_exception=True)
def storagefee_del(request, id):
    log = get_object_or_404(Storagefee,pk=id)
    Operation.objects.create(account=request.user, action='2', description='删除仓租费用方案',
                             content_object=log, object_repr=log)
    log.delete()
    return redirect('storagefee_list')


@login_required()
@permission_required(['depot.add_stockchange','depot.change_stockchange','delete_stockchange'],raise_exception=True)
def stockchange_list(request):
    data = Stockchange.objects.all().order_by('change_time')
    content_type = ContentType.objects.get_for_model(Stockchange)
    # operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request,'stockchange_list.html',{'data':data,})
# def download_file(request):
#     response = StreamingHttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment;filename=export.xls'
#     return response


# @login_required()
# def transorder_sum(request):
#     if request.method == 'POST':
#         #要验证不能有空值、不能是错误的sku、不能sku不存在，sku的状态必须是已审核
#         #前端输入的应该是sku的代码而不是id
#
#         #解析post，用的很笨的办法
#         result = []
#         for n in range(len(request.POST)):
#             index_s = "sku_" + str(n)
#             index_a = "amount_" + str(n)
#             if index_s in request.POST:
#                 each = {request.POST[index_s]:request.POST[index_a]}
#                 result.append(each)
#         #将解析结果在关系表Prediction中依次创建
#         for item in result:
#             for key,value in item.items():
#                     r = Sku.objects.filter(id=int(key),company=request.user.company,status='1')
#                     if len(r) == 0:
#                         errors = "您输入的sku错误，只有通过审核的sku才能添加到运单之中，请检查您的输入。"
#                         t = Transorder.objects.get(id=request.POST['id'])
#                         data = Prediction.objects.filter(transorder=t)
#                         sku_code_list = Sku.objects.filter(company=request.user.company, status='1')
#                         return render(request, 'transorder_sum.html',{
#                             'data': data,
#                             'id': request.POST['id'],
#                             'sku_code_list': sku_code_list,
#                             'errors': errors,
#                             })
#         # 先清空transorder的所有sku数据再保存
#         t = Transorder.objects.get(id=request.POST['id'])
#         t.skus.clear()
#         for item in result:
#             for key,value in item.items():
#                 Prediction.objects.create(transorder=t, sku=Sku.objects.get(id=int(key)), amount=int(value), check=int(value))
#         #返回运单列表
#         data = Transorder.objects.filter(company=request.user.company)
#         return render(request, 'transorder_list.html', {
#             'data': data,
#         })
#     else:
#         t = Transorder.objects.get(id=request.GET['id'])
#         data = Prediction.objects.filter(transorder=t)
#         sku_code_list = Sku.objects.filter(company=request.user.company,status='1')
#         return render(request, 'transorder_sum.html', {'data':data,'id':request.GET['id'],'sku_code_list':sku_code_list})

