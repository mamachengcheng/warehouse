from django.db import models
from account.models import Company, Level
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
# Create your models here.
#仓库管理app，包含以下模型
#1.仓库：仓库id，仓库名称，仓库地址
#2.库位：库位id，库位名称，仓库id
#3.库存：SKU，库位id，数量，入库时间

class Depot(models.Model):
    name = models.CharField(max_length=150, verbose_name='仓库名称', null=False, blank=False, unique=True,
                            error_messages={'unique':'仓库不能重名，您输入的仓库名称已经存在了，请换一个名字。'})
    address = models.CharField(max_length=300, verbose_name='仓库地址', null=True, blank=True)

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = '仓库'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def current(self):
        current_depot = Depot.objects.last()
        return current_depot

class Unit(models.Model):
    depot = models.ForeignKey(Depot, verbose_name='所属仓库' ,on_delete=models.CASCADE)
    name = models.CharField(max_length= 20, verbose_name='库位编号', null=False, blank=False, unique=True)

    class Meta:
        verbose_name = '库位'
        verbose_name_plural = '库位'

    def __str__(self):
        return self.name

class Skutype(models.Model):
    #创建SKU类别
    name = models.CharField(max_length=20, verbose_name='SKU类别', unique=True, blank=False,
                            error_messages={'unique':'SKU类别不能重名，请重新输入SKU类别名称'})

    class Meta:
        verbose_name = 'SKU类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Skutypefee(models.Model):
    #设置不同客户等级对应的SKU类别的费用
    #TODO 对数字为正数要做校验
    level = models.ForeignKey(Level, null=True, default=None, blank=True, on_delete=models.CASCADE)
    skutype = models.ForeignKey(Skutype, null=True, default=None, blank=True, on_delete=models.CASCADE)
    operation_fee = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='操作费', blank=True, default=0,
                                        help_text='请输入正数，输入负数会导致计算错误，保留两位小数')
    in_fee = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='入仓费', blank=True, default=0,
                                 help_text='请输入正数，输入负数会导致计算错误，保留两位小数')

    class Meta:
        verbose_name = 'Sku类别费用'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '客户等级：'+ self.level.__str__() + '-类别：'+ self.skutype.__str__()

    def __repr__(self):
        return '客户等级：' + self.level.__str__() + '-类别：' + self.skutype.__str__()



class Customerlevelfee(models.Model):
    #与客户等级相关的费用
    # TODO 对数字为正数要做校验
    level = models.OneToOneField(Level, verbose_name='客户等级', null=True, on_delete=models.CASCADE, unique=True)
    # 不同客户等级的退件检查费
    reject_check_fee = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='退件接收检查费',
                                           help_text='每单退件收取的接收检查费，请输入正数，输入负数会导致计算错误，保留两位小数',
                                           default=0, blank=True)
    storage_fee = models.PositiveSmallIntegerField(verbose_name='仓租', default=0, blank=True,
                                                 help_text='请输入正整数，此数值用于计算每月每立方米仓租费')

    def __str__(self):
        return '客户等级' + self.level.__str__() + '的费用标准'

    def __repr__(self):
        return '客户等级' + self.level.__str__() + '的费用标准'


class Storagefee(models.Model):
    month = models.PositiveSmallIntegerField(verbose_name='月份',unique=True,help_text='请输入计算仓租的月份，必须是1-12的正整数，且不能重复')
    free_ratio = models.PositiveSmallIntegerField(verbose_name='小于此值免租的区间', help_text='正整数，代表0到此值的区间')
    high_ratio = models.PositiveSmallIntegerField(verbose_name='大于此值按体积来计算的区间',help_text='正整数，代表大于此值的区间')

    def __str__(self):
        return str(self.month) + '月的费用标准'

    def __repr__(self):
        return str(self.month) + '月的费用标准'


class Sku(models.Model):
    # TODO 对数字为正数要做校验
    STATUS_TYPE = (
        ('0', '待审核'),
        ('1', '已审核'),
        ('2', '拒收'),
    )
    name = models.CharField(max_length=50, verbose_name='SKU名称-中文', blank=False, default='')
    name_en = models.CharField(max_length=50, verbose_name='SKU名称-英文', blank=True, default='')
    code = models.CharField(max_length=50, verbose_name='客户SKU编码', blank=False, default='')
    leo_code = models.CharField(max_length=50, verbose_name='雷欧海外仓SKU编码', default='', unique=True)
    status = models.CharField(max_length=12, choices=STATUS_TYPE, verbose_name='Sku状态', default=0)
    declare_code = models.CharField(max_length=50, verbose_name='海关申报代码', blank=True, default='')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='申报价值', blank=True, default=0,
                                help_text='单位：欧元，保留2位小数点')
    img = models.ImageField(upload_to='sku_img', verbose_name='图片', blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='重量', blank=True, default=0,
                                 help_text='单位：kg千克，保留3位小数点')
    volume = models.DecimalField(max_digits=8, decimal_places=6, verbose_name='体积', blank=True, default=0,
                                 help_text='单位：m³立方米，保留6位小数点')
    length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='长度', blank=True, default=0,
                                 help_text='单位：米，保留2位小数点')
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='宽度', blank=True, default=0,
                                 help_text='单位：米，保留2位小数点')
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='高度', blank=True, default=0,
                                 help_text='单位：米，保留2位小数点')
    skutype = models.ForeignKey(Skutype, verbose_name='SKU类别', blank=True, null=True, default=None,
                                on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, verbose_name='所属公司', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    category = models.CharField(max_length=20, verbose_name='品类', blank=True, default='')

    class Meta:
        verbose_name = 'SKU信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code


    @classmethod
    def create_leo_code(self):
        import random
        d = timezone.now()
        prefix = d.strftime("%y%m%d%H%M%S%f")
        tail = random.randrange(100, 999)
        return prefix + str(tail)


    def is_exist(self):
        #是否有库存
        is_exist_quantity = False
        stocks = self.count_set.all()
        for stock in stocks:
            if stock.normal > 0 or stock.preparing_in > 0 or stock.preparing_out > 0 or stock.freeze > 0 or stock.short > 0 or stock.other > 0:
                is_exist_quantity = True
                break
        return is_exist_quantity


    def in_recent_thirty(self):
        #近三十天入库总量
        result_date = timezone.now() - timezone.timedelta(days=30)
        in_sum = self.stockchange_set.filter(change_type='1', change_time__gte=result_date).aggregate(Sum('quantity'))
        if in_sum['quantity__sum'] :
            return in_sum['quantity__sum']
        else:
            return 0


    def out_recent_thirty(self):
        #近三十天出库总量
        result_date = timezone.now() - timezone.timedelta(days=30)
        out_sum = self.stockchange_set.filter(change_type='2', change_time__gte=result_date).aggregate(Sum('quantity'))
        if out_sum['quantity__sum']:
            return out_sum['quantity__sum']
        else:
            return 0

    def sales_recent_thirty(self):
        #近三十天日销量
        res = self.out_recent_thirty()/30
        return float('%.2f' % res)


    def get_current_normal(self):
        #获取当期库存数量
        cur_sum = self.count_set.all().aggregate(Sum('normal'))
        if cur_sum['normal__sum']:
            return cur_sum['normal__sum']
        else:
            return 0

    def sales_delta(self,days):
        result_date = timezone.now() - timezone.timedelta(days=days)
        out_sum = self.stockchange_set.filter(change_type='2', change_time__gte=result_date).aggregate(Sum('quantity'))
        if out_sum['quantity__sum']:
            out_sum =  out_sum['quantity__sum']
        else:
            out_sum = 0
        avg_sales = out_sum / days
        avg_sales = float('%.2f' % avg_sales)
        result = {'out_sum':out_sum,'avg_sales':avg_sales}
        return result



    # def get_absolute_url(self):
    #     from django.core.urlresolvers import reverse
    #     return reverse('sku_examine_list', type='edit')

class Count(models.Model):
    sku = models.ForeignKey(Sku, null=True, on_delete=models.CASCADE, verbose_name='SKU')
    depot = models.ForeignKey(Depot, null=True, default=None, blank=True, on_delete=models.CASCADE, verbose_name='所属仓库')
    unit = models.ForeignKey(Unit, null=True, default=None, blank=True, on_delete=models.SET_NULL, verbose_name='所属库位')
    normal = models.PositiveIntegerField(verbose_name='正常', blank=True, default=0)
    preparing_in = models.PositiveIntegerField(verbose_name='待入库', blank=True, default=0)
    preparing_out = models.PositiveIntegerField(verbose_name='待出库', blank=True, default=0)
    freeze = models.PositiveIntegerField(verbose_name='冻结', blank=True, default=0)
    short = models.PositiveIntegerField(verbose_name='缺货', blank=True, default=0)
    other = models.PositiveIntegerField(verbose_name='其他', blank=True, default=0)

    class Meta:
        verbose_name = 'SKU数量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.normal)

    def __repr__(self):
        return 'SKU:'+self.sku.__str__()+'的数量'

class Transorder(models.Model):
    STATUS_TRANS = (
        ('1','未提交'),
        ('2','已提交'),
        ('3','已验收'),
        ('4','完结'),
    )
    company = models.ForeignKey(Company, verbose_name='所属公司', null=True, default=None, blank=True, on_delete=models.SET_NULL)
    depot = models.ForeignKey(Depot, verbose_name='目标仓库', null=True, default=None, on_delete=models.SET_NULL)
    skus = models.ManyToManyField(Sku, verbose_name='包含货物', through='Prediction')
    date_arrive = models.DateField(verbose_name='预计到达时间')
    transport_code = models.CharField(max_length=50, verbose_name='货运单号', blank=True, default='')
    transport_firm = models.CharField(max_length=50, verbose_name='货运公司', blank=True, default='')
    value_all = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='货值总计', blank=True, default=0)
    remark = models.TextField(max_length=300, verbose_name='备注', blank=True, default='')
    status_trans = models.CharField(choices=STATUS_TRANS, max_length=2,verbose_name='运单状态', default='1')
    check = models.TextField(verbose_name='核对说明', blank=True, default='')
    date_check = models.DateTimeField(auto_now=True, verbose_name='验收时间')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '预计到货订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.transport_code

    def __repr__(self):
        return self.transport_code


class Prediction(models.Model):
    transorder = models.ForeignKey(Transorder, on_delete=models.CASCADE, verbose_name='预计到货货物清单')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, null=True, verbose_name='到货SKU')
    amount = models.PositiveSmallIntegerField(verbose_name='预计到货数量')
    check = models.PositiveSmallIntegerField(blank=True, default=0)

    class Meta:
        verbose_name = '货物数量预报'

    def __str__(self):
        return '到货预报：' + self.sku.__str__() + '，数量：' + str(self.amount)

    def __repr__(self):
        return '到货预报：' + self.sku.__str__() + '，数量：' + str(self.amount)

    def get_unit(self):
        sku_count = get_object_or_404(Count, sku=self.sku, depot=self.transorder.depot)
        return sku_count.unit


class Stockchange(models.Model):
    CHANGE_TYPE = (
        ('1','入库'),
        ('2','出库'),
        ('3','待入库'),
        ('4','收货'),
        ('5','其他'),
        ('6','取消订单'),
    )
    OPERATE_STYLE = (
        ('1','系统'),
        ('2','人工'),
    )
    sku = models.ForeignKey(Sku, verbose_name='SKU', on_delete=models.SET_NULL, null=True)
    depot = models.ForeignKey(Depot, verbose_name='仓库', on_delete=models.SET_NULL, null=True)
    change_type = models.CharField(choices=CHANGE_TYPE, max_length=2, verbose_name='变动类型')
    operate_style = models.CharField(choices=OPERATE_STYLE,max_length=2,verbose_name='操作方式')
    quantity = models.PositiveSmallIntegerField(verbose_name='数量')
    instruction = models.CharField(max_length=300, verbose_name='变动说明', blank=True, default='')
    change_time = models.DateTimeField(auto_now_add=True, verbose_name='变动时间')
    company = models.ForeignKey(Company, verbose_name='客户公司', on_delete=models.SET_NULL, null=True)
