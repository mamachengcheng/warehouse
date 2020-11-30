from django import forms
from depot.models import Sku

class QueryTimeDeltaForm(forms.Form):
    begin_date = forms.DateField(label='起始时间', widget=forms.SelectDateWidget,required=True,
                                 help_text='请选择起始时间')
    end_date = forms.DateField(label='结束时间', widget=forms.SelectDateWidget,required=True,
                               help_text='请选择结束时间')
    sku = forms.ModelChoiceField(queryset=Sku.objects.all(), label='选择SKU',required=True,
                                 help_text='请选择要查询销售状况的SKU')


class QueryLowStockForm(forms.Form):
    # sku = forms.ModelChoiceField(queryset=Sku.objects.all(), label='选择SKU',required=True)
    quantity = forms.IntegerField(label='输入低库存值',required=True, help_text='请输入一个正整数，将查询所有正常库存数量低于此值的SKU')


class QueryStorageForm(forms.Form):
    begin_date = forms.DateField(label='起始时间', widget=forms.SelectDateWidget,required=True,
                                 help_text='请选择起始时间')
    end_date = forms.DateField(label='结束时间', widget=forms.SelectDateWidget,required=True,
                               help_text='请选择结束时间')
