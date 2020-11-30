from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm

from .models import Company,Account,Announcement,Level,Prepayrecord


class CompanyForm(ModelForm):
    #公司信息form
    class Meta:
        model = Company
        fields = ['id','name','address','contacts','contacts_phone','level']



class AccountProfileForm(ModelForm):
    #普通用户资料修改
    class Meta:
        model = Account
        fields = ['nickname','last_name','first_name','phone','email']



class AccountCreationForm(UserCreationForm):
    #这里必须重新指定Meta中的model，否则表单无法使用
    class Meta:
        model = get_user_model()
        fields = ('username',)



class AccountEditForm(ModelForm):
    #管理员编辑账户
    class Meta:
        model = Account
        fields = ['username','nickname','first_name','last_name','is_staff','phone','email','company','is_active', 'groups']
    def __init__(self, *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs['class']='form-control'



class AnnouncementForm(ModelForm):
    #公告form
    class Meta:
        model = Announcement
        fields = ['title','summary','content','status']



class LevelForm(ModelForm):
    #公司等级form
    class Meta:
        model = Level
        fields = '__all__'




class GroupForm(ModelForm):
    #用户组group
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs['class']='form-control'
            if field_name == 'name':
                field.help_text='用户组名称唯一，不可以重复'
            if field_name == 'permissions':
                field.widget.attrs['style']='height:300px;'
                field.help_text='请按住control键鼠标点击进行多选'


class PrepayForm(ModelForm):
    class Meta:
        model = Prepayrecord
        fields = ('sum','instruction','type')


class QueryBillForm(forms.Form):
    YEAR = [(2018,2018),(2019,2019),(2020,2020),(2021,2021)]
    MONTH = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)]
    TYPE = (
        (1, '预存款'),
        (2, '入仓费'),
        (3, '操作费'),
        (4, '订单运费'),
        (5, '仓租'),
        (6, '退件接受检查费'),
        (7, '退件相关'),
        (8, '其他'),
        (9, '所有')
    )
    year = forms.ChoiceField(choices=YEAR, label='年')
    month = forms.ChoiceField(choices=MONTH, label='月')
    type = forms.ChoiceField(choices=TYPE, label='请选择订单状态')


    # def __init__(self, *args, **kwargs):
    #     super(PrepayForm, self).__init__(*args, **kwargs)
    #     for field_name in self.base_fields:
    #         field = self.base_fields[field_name]
    #         field.widget.attrs['class'] = 'form-control'


                # from django.core.exceptions import ValidationError
# #自己编写的创建账户的form，后来使用了内建的UserCreationForm
# class AccountCreateForm(forms.Form):
#     #TODO缺少长度、特殊符号的验证
#     username = forms.CharField(
#         required=True,
#         max_length=50,
#         min_length=6,
#         help_text='请输入用户名，建议采用字母和数字的组合，不能包含特殊符号',
#         widget=forms.TextInput(attrs={'class':'from-control','placeholder':'用户名为6-12个字符'})
#     )
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#     def clean_password_again(self):
#         pass1 = self.cleaned_data.get('password')
#         pass2 = self.cleaned_data.get('password_again')
#         if pass1 != pass2:
#             raise ValidationError('两次输入的密码不一致，请重新输入')
#         return pass1
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         users = Account.objects.filter(username=username).count()
#         if users:
#             raise ValidationError('用户名已经存在，请重新输入')
#         return username
