from django import forms
from django.forms import ModelForm
from .models import *


class DepotForm(ModelForm):
    class Meta:
        model = Depot
        fields = ['name','address']


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['depot','name']


class UnitInitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['depot']

class SkutypeForm(ModelForm):
    class Meta:
        model = Skutype
        fields = ('name',)


class SkuCreateForm(ModelForm):
    class Meta:
        model = Sku
        fields = ('name','company','name_en','code','leo_code','declare_code','price','weight','volume',
                  'length','width','height','category','img')
        widgets = {
            'company': forms.HiddenInput(),
            'leo_code': forms.HiddenInput(),
        }


class SkuEditForm(ModelForm):
    class Meta:
        model = Sku
        fields = ('name','name_en','code','declare_code','skutype','price','weight','volume',
                  'length','width','height','category','img')


class SkuExamineForm(ModelForm):
    class Meta:
        model = Sku
        fields = ('name','name_en','code','declare_code','price','weight','volume','img',
                  'weight','volume','length','width','height','skutype','status','company','category')
        # labels = {
        #     'unit': _('分配库位'),
        # }
        # widgets = {
            # 'unit': forms.TextInput()
            # 'unit': forms.ModelChoiceField(queryset=Unit.objects.filter(depot))
        # }


class TransorderForm(ModelForm):
    class Meta:
        model = Transorder
        fields = ('date_arrive','depot','transport_code','transport_firm','value_all','remark','company')
        widgets = {
            'date_arrive':forms.SelectDateWidget,
            'company': forms.HiddenInput,
        }


class TransFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super(TransFormSet,self).clean()
        if any(self.errors):
            return
        sku_names = []
        for form in self.forms:
            if 'sku' in form.cleaned_data:
                sku_name = form.cleaned_data['sku']
                if sku_name in sku_names:
                    self.errors.append("同一个SKU只能有一条记录，请重新检查")
                    raise forms.ValidationError("同一个SKU只能有一条记录，请重新检查")
                sku_names.append(sku_name)
        # return


class SkutypefeeForm(ModelForm):
    class Meta:
        model = Skutypefee
        fields = '__all__'


class PredictionForm(ModelForm):
    class Meta:
        model = Prediction
        fields = ('sku','amount','check')


class CustomerlevelfeeForm(ModelForm):
    class Meta:
        model = Customerlevelfee
        fields = '__all__'


class SkuUnitForm(ModelForm):
    class Meta:
        model = Count
        fields = ('unit',)


class CountForm(ModelForm):
    class Meta:
        model = Count
        fields = '__all__'


class StoragefeeForm(ModelForm):
    class Meta:
        model = Storagefee
        fields = '__all__'


class SelectCompanyForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all(),required=True,label='')