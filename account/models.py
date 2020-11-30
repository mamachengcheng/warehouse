from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.shortcuts import get_object_or_404
import decimal
from django.utils import timezone

# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=20, verbose_name='公司等级', unique=True,
                            help_text='名称必须唯一，且不能超过20个字符，可以使用中文、英文或数字的组合')

    class Meta:
        verbose_name = '公司等级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, verbose_name='公司名称')
    address = models.CharField(max_length=200, blank=True, default='', verbose_name='公司地址')
    contacts = models.CharField(max_length=20, blank=True, default='', verbose_name='联系人')
    contacts_phone = models.CharField(max_length=20, blank=True, default='', verbose_name='联系电话')
    prepayment =models.DecimalField(max_digits=7, decimal_places=2, verbose_name='预存款', blank=True, default=0)
    level = models.ForeignKey(Level, blank=True, null=True, default=None, verbose_name='公司等级', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


    def get_volume_per_day(self):
        #计算日均体积-每日定时任务触发记录
        skus = self.sku_set.all()
        total_volume = 0
        for sku in skus:
            current_sum = sku.get_current_normal()
            sku_volume_sum = sku.volume * current_sum
            total_volume += sku_volume_sum
        return total_volume


    def get_out_per_day(self):
        #计算日均出库体积-每日定时任务记录
        from depot.models import Stockchange
        current = timezone.now()
        record_out = Stockchange.objects.filter(company=self, change_type='2', change_time__year=current.year, change_time__month=current.month,
                                   change_time__day=current.day)
        total_volume = 0
        for item in record_out:
            volume = item.sku.volume
            quantity = item.quantity
            sku_volumes = volume * quantity
            total_volume += sku_volumes
        return total_volume


    def get_volume_out_month(self,year,month):
        #计算指定月份的总出库体积
        from depot.models import Stockchange
        record_out = Stockchange.objects.filter(company=self,change_type='2',change_time__year=year,change_time__month=month)
        total_volume = 0
        for item in record_out:
            volume = item.sku.volume
            quantity = item.quantity
            sku_volumes = volume * quantity
            total_volume += sku_volumes
        return total_volume


    @classmethod
    def month_days(self,year,month):
        #返回指定月份的天数
        import calendar
        monthrange = calendar.monthrange(year,month)
        return monthrange[1]


    def month_ratio(self,year,month):
        #计算月周转率

        #先计算日均体积总和
        volume_sum = Companyvolumeperday.objects.filter(company=self,date__year=year,date__month=month).aggregate(Sum('volume'))
        if volume_sum['volume__sum']:
            volume_sum = volume_sum['volume__sum']
        else:
            volume_sum = 0
        #获得当月天数
        month_has_days = Company.month_days(year,month)
        # 计算日均库存体积
        volume_avg = volume_sum / month_has_days
        # 当月出库总体积为
        volume_out = self.get_volume_out_month(year,month)
        # 计算月周转率:当月日均库存/当月出库总体积
        if volume_out > 0:
            ratio = volume_avg / volume_out
        else:
            ratio = 0
        # 返回 日均库存体积-月出库体积 和 月周转率
        plus = decimal.Decimal(volume_avg) - decimal.Decimal(volume_out)
        result = {'plus': plus, 'ratio' : ratio,'quotiety':round(ratio),'volume_avg': volume_avg }
        return result


    def count_storage_fee(self,year,month):
        #获取月份费用参数
        storage_fee = 0
        from depot.models import Storagefee
        x = get_object_or_404(Storagefee,month=month)
        small = x.free_ratio
        big = x.high_ratio
        #获取计算参数
        result = self.month_ratio(year,month)
        plus = result['plus']
        ratio = result['ratio']
        quotiety = result['quotiety']
        volume_avg = result['volume_avg']
        #判断所处区间，进行三种不同方式的计算
        if ratio > 0 and ratio <= small:
            storage_fee = 0
        elif ratio > small and ratio <= big:
            storage_fee = plus * quotiety
            #storage_fee = decimal.Decimal(storage_fee)
        else:
            from depot.models import Customerlevelfee
            level_fee = get_object_or_404(Customerlevelfee,level=self.level)
            storage_fee = volume_avg * level_fee.storage_fee
            #storage_fee = decimal.Decimal(storage_fee)
        return storage_fee


class Account(AbstractUser):
    is_staff = models.BooleanField(max_length=10,verbose_name='是否仓库管理员', blank=True, default=False,
                                   help_text='请选择该账户是否属于仓库管理员。注意！请不要指定一个用户是仓库管理员的同时还属于某个公司！')
    nickname = models.CharField('昵称', max_length=20, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default='', verbose_name='电话号码')
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='所属公司', on_delete=models.SET_NULL,
                                help_text='请指定该账户属于哪个公司。注意！请不要指定一个用户是仓库管理员的同时还属于某个公司！')
    #在此扩展用户信息
    #BUG-在admin后台创建用户无法调用creatuse方法，密码不能hash

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


#操作记录模型
class Operation(models.Model):
    OPERATION_ACTION = (
        ('0', '其他'),
        ('1', '新建'),
        ('2', '删除'),
        ('3', '修改'),
        ('4', '查询'),
        ('5', '审核SKU'),
        ('6', '提交到货预报'),
        ('7', '审核到货预报'),
        ('8', '入库'),
        ('9', '出库'),
        ('10','手动修改库存'),
        ('11','订单完结'),
        ('12','取消订单'),
    )
    account = models.ForeignKey(Account, verbose_name='操作者', null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=8, choices=OPERATION_ACTION, verbose_name='动作')
    description = models.CharField(max_length=200, verbose_name='描述', blank=True, default='')
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, default='')
    content_object = GenericForeignKey('content_type', 'object_id')
    action_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '操作记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description


#公告模型
class Announcement(models.Model):
    STATUS = (
        (1,'保存'),
        (2,'发布'),
        (3,'撤回')
    )
    account = models.ForeignKey(Account, verbose_name='发布人', null=True, default=None, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, verbose_name='公告标题')
    summary = models.CharField(max_length=200, verbose_name='简介')
    content = models.TextField(verbose_name='公告内容')
    publish_time = models.DateTimeField(auto_now=True, verbose_name='发布时间')
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, default=1,verbose_name='公告状态')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name


#预存款变更记录模型
class Prepayrecord(models.Model):
    TYPE =(
        (1,'预存款'),
        (2,'入仓费'),
        (3,'操作费'),
        (4,'订单运费'),
        (5,'仓租'),
        (6,'退件接受检查费'),
        (7,'退件相关'),
        (8,'其他')
    )
    from depot.models import Transorder
    from order.models import Order,Reject
    company = models.ForeignKey(Company, null=True,blank=True, default=None, on_delete=models.SET_NULL)
    account = models.ForeignKey(Account, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    transorder = models.ForeignKey(Transorder, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    reject = models.ForeignKey(Reject, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    sum = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='金额',
                              help_text='请输入发生金额，扣款以负数表示，如：-12.5')
    instruction = models.CharField(max_length=100, verbose_name='说明', default='', blank=True,
                                   help_text="请输入费用发生的详细原因，便于后期记录查找")
    type = models.SmallIntegerField(choices=TYPE, verbose_name='费用类别',
                                    help_text="请在预设的费用类别中选择发生的费用所属的类别")
    time = models.DateTimeField(auto_now=True, verbose_name='触发时间')

    def __str__(self):
        return self.instruction

    def __repr__(self):
        return self.instruction

    class Meta:
        verbose_name = '费用记录'
        verbose_name_plural = verbose_name


class Companyvolumeperday(models.Model):
    company = models.ForeignKey(Company, verbose_name='客户公司',on_delete=models.CASCADE)
    volume = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='当日库存体积', blank=True, default=0)
    out = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='当日出库体积', blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True, verbose_name='日期')

    class Meta:
        verbose_name = '公司每日库存体积'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     date_str = self.date.strftime("%Y-%m-%d")
    #     return ('客户%s在%s的当日库存体积为%s立方米' % (self.company.name, date_str, str(self.volume)))
    #
    # def __repr__(self):
    #     date_str = self.date.strftime("%Y-%m-%d")
    #     return ('客户%s在%s的当日库存体积为%s立方米' % (self.company.name, date_str, str(self.volume)))




