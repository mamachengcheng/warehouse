from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from .models import Order, Delivery, Reject, Orderspecial
from depot.models import Count,Sku,Depot,Company



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('company','sales_record_number', 'user_id', 'buyer_full_name', 'buyer_phone_number', 'buyer_email',
         'buyer_address1', 'buyer_address2', 'buyer_city', 'buyer_postcode', 'buyer_country', 'delivery_service',
                  'depot',)
        widgets = {
            'company': forms.HiddenInput()
        }


class OrderContainFormSet(forms.models.BaseInlineFormSet):
    # TODO 当前不严谨的地方：运单和订单客户选择的是SKU的名字，名字重复的问题
    # TODO 校验数量时，依据只是SKU名字，不严谨
    # TODO 涉及SKU处理的地方应该统一使用SKU的leo_code,保证唯一性
    # TODO 错误信息如何传递到对应的field，而不是对应全局
    # TODO 多仓库的情况下，根据SKU从count中会取出多个数值，目前多仓库不适用
    def clean(self):
        super(OrderContainFormSet,self).clean()
        if any(self.errors):
            return
        sku_codes = []
        for form in self.forms:
            print(form.cleaned_data)
            if 'order' in form.cleaned_data:
                order = form.cleaned_data['order']
                company = order.company
            if 'sku' in form.cleaned_data:
                sku_code = form.cleaned_data['sku'].code
                sku = get_object_or_404(Sku,code=sku_code,company=company)
                try:
                    quantity_ok = Count.objects.get(sku=sku,depot=Depot.current())
                except:
                    self.errors.append("SKU:"+sku_code+" 没有库存，请重新检查")
                    raise forms.ValidationError("SKU:"+sku_code+" 没有库存，请重新检查")
                if quantity_ok.normal < form.cleaned_data['amount']:
                    self.errors.append("SKU:"+sku_code+" 库存数量不足，请重新检查")
                    raise forms.ValidationError("SKU:"+sku_code+" 库存数量不足，请重新检查")
                if sku_code in sku_codes:
                    self.errors.append("同一个SKU:"+sku_code+" 只能有一条记录，请重新检查")
                    raise forms.ValidationError("同一个SKU:"+sku_code+" 只能有一条记录，请重新检查")
                sku_codes.append(sku_code)


class OrderImportForm(forms.Form):
    excel_file = forms.FileField(label='请选择要导入的文件',)


class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'


class RejectForm(ModelForm):
    class Meta:
        model = Reject
        fields = ('company', 'sales_record_number', 'user_id', 'buyer_full_name', 'buyer_phone_number', 'buyer_email',
              'buyer_address1', 'buyer_address2', 'buyer_city', 'buyer_postcode', 'buyer_country', 'delivery_service',
              'depot','delivery_code','remarks')


class OrderspecialForm(ModelForm):
    class Meta:
        model = Orderspecial
        fields = '__all__'


class SelectCompanyAndStatusForm(forms.Form):
    STATUS = (
        ('1', '所有'),
        ('2', '已提交'),
        ('3', '已处理'),
        # ('4', '已出库'),
        ('5', '已完结'),
        ('7', '其他'),
    )
    company = forms.ModelChoiceField(queryset=Company.objects.all(), label='请选择公司', empty_label='全部', required=False)
    status = forms.ChoiceField(choices=STATUS, label='请选择订单状态')


class SelectStatusForm(forms.Form):
    STATUS = (
        ('1', '未提交'),
        ('2', '已提交'),
        ('3', '已处理'),
        # ('4', '已出库'),
        ('5', '已完结'),
        ('6', '问题单'),
        ('7', '其他'),
        ('8', '全部')
    )
    status = forms.ChoiceField(choices=STATUS, label='请选择订单状态')


class ExportOrderForm(forms.Form):
    STATUS = (
        ('1', '未提交'),
        ('2', '已提交'),
        ('3', '已处理'),
        # ('4', '已出库'),
        ('5', '已完结'),
        ('6', '问题单'),
        ('7', '其他'),
        ('8', '全部')
    )

    begin_date = forms.DateField(label='起始时间', widget=forms.SelectDateWidget,required=True,
                                 help_text='请选择起始时间')
    end_date = forms.DateField(label='结束时间', widget=forms.SelectDateWidget,required=True,
                               help_text='请选择结束时间')
    status = forms.ChoiceField(choices=STATUS, label='请选择订单状态')