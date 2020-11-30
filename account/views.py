from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from decimal import *
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import xlwt


from .models import *
from .forms import *
# Create your views here.


@login_required()
def company_list(request):
    companys = Company.objects.all()
    content_type = ContentType.objects.get_for_model(Company)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'company_list.html', {'companys':companys,'op':operate_record})


@login_required()
@permission_required(['account.change_company','account.add_company'],raise_exception=True)
def company_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = CompanyForm()
        else:
            old = get_object_or_404(Company,pk=id)
            form = CompanyForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'company_edit.html', context)
    else:
        if id == 0:
            new = CompanyForm(request.POST)
            mess = '新公司添加成功！'
            action_id = '1'
            des = '创建新公司'
        else:
            old = Company.objects.get(id=id)
            new = CompanyForm(request.POST, instance=old)
            mess = '公司信息修改成功！'
            action_id = '3'
            des = '修改公司信息'
        if new.is_valid():
            log = new.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'company_edit.html', {'form': new,'id':id})
        return redirect('company_list')


@login_required()
@permission_required('account.delete_company',raise_exception=True)
def company_del(request,id):
    if request.method == 'POST':
        log = get_object_or_404(Company,pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除公司', content_object=log,
                                 object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '公司删除成功！')
        return redirect('company_list')



@login_required()
def account_list(request):
    if request.user.is_staff:
        # if 'check_company_member' in request.GET:
        #     users = Account.objects.filter(company_id=request.GET['check_company_member'])
        # else:
        users = Account.objects.all()
        content_type = ContentType.objects.get_for_model(Account)
        operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    else:
        users = Account.objects.filter(company = request.user.company)
        content_type = ContentType.objects.get_for_model(Account)
        operate_record = Operation.objects.filter(content_type=content_type,account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'account_list.html', {'data':users, 'op':operate_record})


@login_required()
@permission_required('account.delete_account',raise_exception=True)
def account_del(request,id):
    if request.method == 'POST':
        log = get_object_or_404(Account,pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除用户', content_object=log,
                                 object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '用户删除成功！')
        return redirect('account_list')


@login_required()
@permission_required('account.add_account',raise_exception=True)
def account_create(request):
    #创建账户，只创建用户名和密码
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            log = form.save()
            if request.user.company:
                log.company = request.user.company
                log.save()
            Operation.objects.create(account=request.user, action='1', description='创建用户', content_object=log,
                                     object_repr=log)
            return redirect('account_list')
        else:
            return render(request, 'account_create.html', {'form': form})
    else:
        form = AccountCreationForm()
        return render(request, 'account_create.html', {'form': form})


@login_required()
@permission_required('account.change_account',raise_exception=True)
def account_edit(request,id):
    old = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance=old)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='3', description='编辑用户', content_object=log,
                                     object_repr=log)
            return redirect('account_list')
        else:
            return render(request, 'account_edit.html', {'form': form, 'id': id})
    else:
        form = AccountEditForm(instance=old)
        return render(request, 'account_edit.html', {'form':form,'id':id})


@login_required()
@permission_required('account.change_account',raise_exception=True)
def password_set(request,id):
    #管理员重置用户密码
    if request.method == 'POST':
        user = Account.objects.get(pk=id)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            log = form.save()
            Operation.objects.create(account=request.user, action='3', description='重置用户密码', content_object=log,
                                     object_repr=log)
            users = Account.objects.all()
            return redirect('account_list')
        else:
            return render(request, 'password_set.html', {'form': form, 'id': id})
    else:
        user = Account.objects.get(pk=id)
        form = SetPasswordForm(user)
        return render(request, 'password_set.html', {'form': form, 'id': id})


@login_required()
def password_change(request):
    #当前用户修改密码
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                users = Account.objects.all()
            else:
                users = Account.objects.filter(company = request.user.company)
            return redirect('backend:index')
        else:
            return render(request, 'password_change.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'password_change.html', {'form': form})


@login_required()
def account_profile(request,id):
    #当前用户编辑个人资料，所有用户都相同
    if request.method == 'POST':
        old = get_object_or_404(Account,pk=id)
        form = AccountProfileForm(request.POST, instance=old)
        if form.is_valid:
            form.save()
            return redirect('backend:index')
        else:
            return render(request, 'account_profile.html', {'form': form, 'id': id})
    else:
        old = get_object_or_404(Account,pk=id)
        form = AccountProfileForm(instance=old)
        return render(request, 'account_profile.html', {'form': form, 'id': id})


# @login_required()
# @permission_required(['account.add_announcement','account.change_announcement','account.delete_announcement'],raise_exception=True)
# def announcement_list(request, type='list'):
#     if type == 'create':
#         if request.method == 'GET':
#             form = AnnouncementForm()
#             return render(request, 'announcement_edit.html', {
#                 'form': form,
#                 'type_type': 'create',
#             })
#         if request.method == 'POST':
#             new = AnnouncementForm(request.POST)
#             if new.is_valid():
#                 log = new.save()
#                 log.account = request.user
#                 log.save()
#                 messages.add_message(request, messages.SUCCESS, '公告添加成功！')
#                 Operation.objects.create(account=request.user, action='1', description='创建公告', content_object=log, object_repr=log)
#             else:
#                 return render(request, 'announcement_edit.html', {
#                     'form': new,
#                     'type_type': 'create',
#                     })
#             data = Announcement.objects.all()
#             return render(request, 'announcement_list.html', {
#                 'data': data,
#             })
#     elif type == 'edit':
#         if request.method == 'GET':
#             old = Announcement.objects.get(id=request.GET['id'])
#             form = AnnouncementForm(instance=old)
#             return render(request, 'announcement_edit.html', {
#                 'form': form,
#                 'type_type': 'edit',
#                 'id': request.GET['id'],
#             })
#         if request.method == 'POST':
#             old = Announcement.objects.get(id=request.POST['id'])
#             new = AnnouncementForm(request.POST, instance=old)
#             if new.is_valid():
#                 log = new.save()
#                 log.account = request.user
#                 log.save()




@login_required()
def announcement_list(request):
    data = Announcement.objects.all().order_by('publish_time')
    content_type = ContentType.objects.get_for_model(Announcement)
    operate_record = Operation.objects.filter(content_type=content_type, account_id=request.user.id).order_by('-action_time')[:10]
    return render(request, 'announcement_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['account.change_announcement','account.add_announcement'],raise_exception=True)
def announcement_edit(request,id=0):
    if request.method == 'GET':
        if id == 0:
            form = AnnouncementForm()
        else:
            old = get_object_or_404(Announcement,pk=id)
            form = AnnouncementForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'announcement_edit.html', context)
    else:
        if id == 0:
            new = AnnouncementForm(request.POST)
            mess = '新公告添加成功！'
            action_id = '1'
            des = '创建新公告'
        else:
            old = Announcement.objects.get(id=id)
            new = AnnouncementForm(request.POST, instance=old)
            mess = '公告修改成功！'
            action_id = '3'
            des = '修改公告'
        if new.is_valid():
            log = new.save()
            log.account = request.user
            log.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'announcement_edit.html', {'form': new,'id':id})
        return redirect('announcement_list')


@login_required()
@permission_required('account.delete_announcement',raise_exception=True)
def announcement_del(request,id):
    if request.method == 'POST':
        log = get_object_or_404(Announcement,pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除公告', content_object=log,
                                 object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '公告删除成功！')
        return redirect('announcement_list')


@login_required()
def announcement_item(request,id):
    item = get_object_or_404(Announcement,pk=id)
    announcements = Announcement.objects.filter(status=2).order_by('-publish_time')[:5]
    return render(request, 'announcement_item.html', {'item':item,'anno':announcements})


@login_required()
@permission_required('account.delete_announcement',raise_exception=True)
def announcement_batch_del(request):
    #批量删除公告
    target = request.POST.getlist('data[]')
    for item in target:
        log = Announcement.objects.get(id=int(item))
        Operation.objects.create(account=request.user, action='2', description='删除公告', content_object=log,
                                 object_repr=log)
        log.delete()
    return redirect('announcement_list')


@login_required()
def level_list(request):
    data = Level.objects.all()
    content_type = ContentType.objects.get_for_model(Level)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request, 'level_list.html', {'data': data,'op':operate_record})


@login_required()
@permission_required('account.delete_levle',raise_exception=True)
def level_del(request,id):
    if request.method == 'POST':
        log = get_object_or_404(Level,pk=id)
        Operation.objects.create(account=request.user, action='2', description='删除公司等级', content_object=log,
                                 object_repr=log)
        log.delete()
        messages.add_message(request, messages.SUCCESS, '公司等级删除成功！')
        return redirect('level_list')


@login_required()
@permission_required(['account.change_level','account.add_level'], raise_exception=True)
def level_edit(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = LevelForm()
        else:
            old = get_object_or_404(Level,pk=id)
            form = LevelForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'level_edit.html', context)
    else:
        if id == 0:
            new = LevelForm(request.POST)
            mess = '新的客户等级添加成功！'
            action_id = '1'
            des = '创建新分级'
        else:
            old = Level.objects.get(id=id)
            new = LevelForm(request.POST, instance=old)
            mess = '客户等级修改成功！'
            action_id = '3'
            des = '修改客户等级'
        if new.is_valid():
            log = new.save()
            log.account = request.user
            log.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'level_edit.html', {'form': new,'id':id})
        return redirect('level_list')


@login_required()
def group_list(request):
    data = Group.objects.all()
    content_type = ContentType.objects.get_for_model(Group)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-action_time')[:10]
    return render(request, 'group_list.html', {'data': data,'op':operate_record})


@login_required()
@permission_required('account.delete_group',raise_exception=True)
def group_del(request,id):
    log = get_object_or_404(Group,pk=id)
    Operation.objects.create(account=request.user, action='2', description='删除用户组', content_object=log,
                             object_repr=log)
    log.delete()
    messages.add_message(request, messages.SUCCESS, '用户组删除成功！')
    return redirect('group_list')


@login_required()
@permission_required(['account.add_group','account.change_group'],raise_exception=True)
def group_edit(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = GroupForm()
        else:
            old = get_object_or_404(Group,pk=id)
            form = GroupForm(instance=old)
        context = {'form':form, 'id':id}
        return render(request, 'group_edit.html', context)
    else:
        if id == 0:
            new = GroupForm(request.POST)
            mess = '新的用户组添加成功！'
            action_id = '1'
            des = '创建新用户组'
        else:
            old = Group.objects.get(id=id)
            new = GroupForm(request.POST, instance=old)
            mess = '用户组修改成功！'
            action_id = '3'
            des = '修改用户组'
        if new.is_valid():
            log = new.save()
            log.account = request.user
            log.save()
            messages.add_message(request, messages.SUCCESS, mess)
            Operation.objects.create(account=request.user, action=action_id, description=des, content_object=log,
                                     object_repr=log)
        else:
            return render(request, 'group_edit.html', {'form': new,'id':id})
        return redirect('group_list')

@login_required()
def companyfee_list(request):
    data = Company.objects.all()
    content_type = ContentType.objects.get_for_model(Prepayrecord)
    operate_record = Operation.objects.filter(content_type=content_type).order_by('-id')[:10]
    return render(request, 'companyfee_list.html', {'data':data,'op':operate_record})


@login_required()
@permission_required(['account.add_prepayrecord','change_prepayrecord'],raise_exception=True)
def companyfee_edit(request,id):
    if request.method == 'POST':
        form = PrepayForm(request.POST)
        company = get_object_or_404(Company, pk=id)
        if form.is_valid():
            record = form.save()
            record.company = company
            record.account = request.user
            record.save()
            #更新公司表中的当前余额
            company.prepayment = company.prepayment + Decimal(request.POST['sum'])
            company.save()
            Operation.objects.create(account=request.user, action='1', description='修改公司预付费', content_object=record,
                                     object_repr=record)
            data = Company.objects.all()
            return render(request, 'companyfee_list.html', {'data': data})
        else:
            return render(request, 'companyfee_edit.html', {
                'company': company,
                'form': form,
            })
    else:
        form = PrepayForm()
        company = get_object_or_404(Company,pk=id)
        return render(request,'companyfee_edit.html',{
            'company': company,
            'form': form,
            'id': id,
        })


@login_required()
def companyfee_item(request,id):
    data = Prepayrecord.objects.filter(company_id=id).order_by('-id')
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    form = QueryBillForm()
    # return render(request,'companyfee_item.html', {'data':data, 'form':form, 'id':id, 'contacts':contacts})
    return render(request,'companyfee_item.html', {'form':form, 'id':id, 'contacts':contacts})


@login_required()
def download_prepayrecord(request,id):
    data = Prepayrecord.objects.filter(company_id=id).order_by('id')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=prepayrecord.xls'
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    row0 = ['序号','发生时间','类别','发生额','客户平台订单号','雷欧订单号','说明']
    for i in range(0, len(row0)):
        sheet.write(0,i,row0[i])
    row = 1
    for i in range(0, len(data)):
        sheet.write(row,0,i+1)
        sheet.write(row,1,data[i].time.strftime('%Y-%m-%d %H:%M:%S'))
        sheet.write(row,2,data[i].get_type_display())
        sheet.write(row,3,data[i].sum)
        if data[i].order:
            sheet.write(row, 4, data[i].order.sales_record_number)
            sheet.write(row, 5, data[i].order.order_code)
        else:
            sheet.write(row, 4, '')
            sheet.write(row, 5, '')
        sheet.write(row,6,data[i].instruction)
        row = row + 1
    workbook.save(response)
    return response


@login_required()
def query_bill(request,id):
    form = QueryBillForm(request.GET)
    year = form.data['year']
    month = form.data['month']
    type = form.data['type']
    if type == '9':
        data = Prepayrecord.objects.filter(company_id=id, time__year=year, time__month=month).order_by('-id')
    else:
        data = Prepayrecord.objects.filter(company_id=id, time__year=year, time__month=month, type=type).order_by('-id')
    paginator = Paginator(data, 25)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'query_bill.html', {'contacts':contacts,'year':year,'month':month,'id':id,'type':type})


@login_required()
def download_bill(request,id,year,month,type):
    if type == '9':
        data = Prepayrecord.objects.filter(company_id=id, time__year=year, time__month=month).order_by('id')
    else:
        data = Prepayrecord.objects.filter(company_id=id, time__year=year, time__month=month, type=type).order_by('-id')
    filename = 'bill-' + str(year) + str(month) + '.xls'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+filename
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    row0 = ['序号', '发生时间', '类别', '发生额', '客户平台订单号', '雷欧订单号', '说明']
    for i in range(0, len(row0)):
        sheet.write(0,i,row0[i])
    row = 1
    for i in range(0, len(data)):
        sheet.write(row, 0, i + 1)
        sheet.write(row, 1, data[i].time.strftime('%Y-%m-%d %H:%M:%S'))
        sheet.write(row, 2, data[i].get_type_display())
        sheet.write(row, 3, data[i].sum)
        if data[i].order:
            sheet.write(row, 4, data[i].order.sales_record_number)
            sheet.write(row, 5, data[i].order.order_code)
        else:
            sheet.write(row, 4, '')
            sheet.write(row, 5, '')
        sheet.write(row, 6, data[i].instruction)
        row = row + 1
    workbook.save(response)
    return response


@login_required()
def account_operate_record(request):
    #当前用户的操作记录
    operate_record = Operation.objects.filter(account_id=request.user.id).order_by('-action_time')
    return render(request,'account_operate_record.html',{'op':operate_record})

