from django.db import models
from account.models import Account, Company, Level
from depot.models import Sku, Skutypefee, Depot
from django.utils import timezone
from django.shortcuts import render,get_object_or_404


# Create your models here.
class Delivery(models.Model):
    level = models.ForeignKey(Level, verbose_name='所属客户等级', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, verbose_name='物流中文名称-CN')
    name_en = models.CharField(max_length=40, verbose_name='物流英文名称-EN', blank=True, default='')
    instruction = models.CharField('备注', max_length=100, blank=True, default='')
    one = models.DecimalField('0.000-0.020',max_digits=5, decimal_places=2, blank=True, default=0)
    two = models.DecimalField('0.021-0.050', max_digits=5, decimal_places=2, blank=True, default=0)
    three = models.DecimalField('0.051-0.100', max_digits=5, decimal_places=2, blank=True, default=0)
    four = models.DecimalField('0.101-0.250', max_digits=5, decimal_places=2, blank=True, default=0)
    five = models.DecimalField('0.251-0.500', max_digits=5, decimal_places=2, blank=True, default=0)
    six = models.DecimalField('0.501-0.750', max_digits=5, decimal_places=2, blank=True, default=0)
    seven = models.DecimalField('0.751-1.000', max_digits=5, decimal_places=2, blank=True, default=0)
    eight = models.DecimalField('1.001-2.000', max_digits=5, decimal_places=2, blank=True, default=0)
    nine = models.DecimalField('2.001-3.000', max_digits=5, decimal_places=2, blank=True, default=0)
    ten = models.DecimalField('3.001-4.000', max_digits=5, decimal_places=2, blank=True, default=0)
    eleven = models.DecimalField('4.001-5.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twelve = models.DecimalField('5.001-6.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirteen = models.DecimalField('6.001-7.000', max_digits=5, decimal_places=2, blank=True, default=0)
    fourteen = models.DecimalField('7.001-8.000', max_digits=5, decimal_places=2, blank=True, default=0)
    fifiteen = models.DecimalField('8.001-9.000', max_digits=5, decimal_places=2, blank=True, default=0)
    sixteen = models.DecimalField('9.001-10.000', max_digits=5, decimal_places=2, blank=True, default=0)
    seventeen = models.DecimalField('10.001-11.000', max_digits=5, decimal_places=2, blank=True, default=0)
    eighteen = models.DecimalField('11.001-12.000', max_digits=5, decimal_places=2, blank=True, default=0)
    nineteen = models.DecimalField('12.001-13.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty = models.DecimalField('13.001-14.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_one = models.DecimalField('14.001-15.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_two = models.DecimalField('15.001-16.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_three = models.DecimalField('16.001-17.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_four = models.DecimalField('17.001-18.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_five = models.DecimalField('18.001-19.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_six = models.DecimalField('19.001-20.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_seven = models.DecimalField('20.001-21.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_eight = models.DecimalField('21.001-22.000', max_digits=5, decimal_places=2, blank=True, default=0)
    twenty_nine = models.DecimalField('22.001-23.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty = models.DecimalField('23.001-24.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_one = models.DecimalField('24.001-25.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_two = models.DecimalField('25.001-26.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_three = models.DecimalField('26.001-27.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_four = models.DecimalField('27.001-28.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_five = models.DecimalField('28.001-29.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_six = models.DecimalField('29.001-30.000', max_digits=5, decimal_places=2, blank=True, default=0)
    thirty_seven = models.DecimalField('30.001-', max_digits=5, decimal_places=2, blank=True, default=0,
                                       help_text='此处为30KG以上的货物运费计算方式，在29.001-30.000的基础上，'
                                                 '每公斤增加的运费，小数位向上取整')

    class Meta:
        verbose_name = '物流运费'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_price(self, weight):
        if weight > 0 and weight <= 0.020:
            return self.one
        elif weight > 0.020 and weight <= 0.050:
            return self.two
        elif weight > 0.050 and weight <= 0.100:
            return self.three
        elif weight > 0.100 and weight <= 0.250:
            return self.four
        elif weight > 0.250 and weight <= 0.500:
            return self.five
        elif weight > 0.500 and weight <= 0.750:
            return self.six
        elif weight > 0.750 and weight <= 1.000:
            return self.seven
        elif weight > 1.000 and weight <= 2.000:
            return self.eight
        elif weight > 2.000 and weight <= 3.000:
            return self.nine
        elif weight > 3.000 and weight <= 4.000:
            return self.ten
        elif weight > 4.000 and weight <= 5.000:
            return self.eleven
        elif weight > 5.000 and weight <= 6.000:
            return self.twelve
        elif weight > 6.000 and weight <= 7.000:
            return self.thirteen
        elif weight > 7.000 and weight <= 8.000:
            return self.fourteen
        elif weight > 8.000 and weight <= 9.000:
            return self.fifiteen
        elif weight > 9.000 and weight <= 10.000:
            return self.sixteen
        elif weight > 10.000 and weight <= 11.000:
            return self.seventeen
        elif weight > 11.000 and weight <= 12.000:
            return self.eighteen
        elif weight > 12.000 and weight <= 13.000:
            return self.nineteen
        elif weight > 13.000 and weight <= 14.000:
            return self.twenty
        elif weight > 14.000 and weight <= 15.000:
            return self.twenty_one
        elif weight > 15.000 and weight <= 16.000:
            return self.twenty_two
        elif weight > 16.000 and weight <= 17.000:
            return self.twenty_three
        elif weight > 17.000 and weight <= 18.000:
            return self.twenty_four
        elif weight > 18.000 and weight <= 19.000:
            return self.twenty_five
        elif weight > 19.000 and weight <= 20.000:
            return self.twenty_six
        elif weight > 20.000 and weight <= 21.000:
            return self.twenty_seven
        elif weight > 21.000 and weight <= 22.000:
            return self.twenty_eight
        elif weight > 22.000 and weight <= 23.000:
            return self.twenty_nine
        elif weight > 23.000 and weight <= 24.000:
            return self.thirty
        elif weight > 24.000 and weight <= 25.000:
            return self.thirty_one
        elif weight > 25.000 and weight <= 26.000:
            return self.thirty_two
        elif weight > 26.000 and weight <= 27.000:
            return self.thirty_three
        elif weight > 27.000 and weight <= 28.000:
            return self.thirty_four
        elif weight > 28.000 and weight <= 29.000:
            return self.thirty_five
        elif weight > 29.000 and weight <= 30.000:
            return self.thirty_six
        elif weight > 30.000:
            import math
            return self.thirty_six + math.ceil(weight - 30) * self.thirty_seven
        else:
            return 0


class Order(models.Model):
    #TODO 下单时库存足够，但出库时库存不足的情况如何处理
    STATUS = (
        ('1','未提交'),
        ('2','已提交'),
        ('3','已处理'),
        # 已废弃状态4 已出库
        ('4','已出库'),
        ('5','已完结'),
        ('6','问题单'),
        ('7','其他'),
    )
    company = models.ForeignKey(Company, verbose_name='所属公司', on_delete=models.SET_NULL, null=True)
    depot =models.ForeignKey(Depot, verbose_name='出货仓库', null=True, on_delete=models.SET_NULL)
    sales_record_number = models.CharField(max_length=80, verbose_name='客户销售平台订单号')
    user_id = models.CharField(max_length=80, verbose_name='客户平台消费者id', blank=True, default='')
    buyer_full_name = models.CharField(max_length=100, verbose_name='消费者姓名')
    buyer_phone_number = models.CharField(max_length=50, verbose_name='消费者联系电话')
    buyer_email = models.EmailField(max_length=200, verbose_name='消费者电子邮箱', blank=True, default='')
    buyer_address1 = models.CharField(max_length=200, verbose_name='消费者地址1')
    buyer_address2 = models.CharField(max_length=200, verbose_name='消费者地址2', blank=True, default='')
    buyer_city = models.CharField(max_length=80, verbose_name='City/Town')
    buyer_county = models.CharField(max_length=80, verbose_name='County', default='')
    buyer_country = models.CharField(max_length=80, verbose_name='Country')
    buyer_postcode = models.CharField(max_length=20, verbose_name='消费者邮编')
    status = models.CharField(choices=STATUS, max_length=1, verbose_name='订单状态', blank=True, default='1')
    order_code = models.CharField(max_length=24,verbose_name='订单编号', blank=True, default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')
    custom_lable = models.ManyToManyField(Sku, through='Ordercontain')
    delivery_service = models.ForeignKey(Delivery, verbose_name='物流服务', null=True, default=None, blank=False, on_delete=models.SET_NULL)
    delivery_code = models.CharField(max_length=80, verbose_name='物流单号', default='')
    final_weight = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='最终重量', default=0)
    final_delivery_fee = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='最终运费', default=0)
    # comment = models.ForeignKey('Ordercomment', null=True, default=None, blank=True)
    #由于Orderdelivery还没有创建，所以使用字符串名字而不是对象
    # delivery_service = models.ForeignKey('Orderdelivery', verbose_name='物流服务', null=True, default=None, blank=True)
    # quantity = models.SmallIntegerField(verbose_name='数量')
    # custom_lable = models.CharField(max_length=20, verbose_name='订单物品SKU')
    # sale_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='售价', blank=True, default=0)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural =  verbose_name

    def __str__(self):
        return self.sales_record_number

    def __repr__(self):
        return self.sales_record_number

    def get_op_fee(self):
        from account.models import Prepayrecord
        op_fee = 0
        try:
            pay_record = get_object_or_404(Prepayrecord, order=self, type='3')
            op_fee = -(pay_record.sum)
        except:
            pass
        return op_fee

    def total_weight(self):
        skus = self.ordercontain_set.all()
        total_weight = 0
        fee = 0
        for item in skus:
            each_weight = item.sku.weight * item.amount
            total_weight += each_weight
        return total_weight

    def delivery_fee(self):
        fee = 0
        try:
            fee = self.delivery_service.get_price(self.total_weight())
        except:
            pass
        return fee

    def count_final_delivery_fee(self):
        fee = 0
        try:
            fee = self.delivery_service.get_price(self.final_weight)
        except:
            pass
        return fee

    def operation_fee(self):
        skus = self.ordercontain_set.all()
        fee = 0
        each_fee = 0
        for item in skus:
            sku_type = item.sku.skutype
            level = self.company.level
            try:
                st = Skutypefee.objects.get(level=level, skutype=sku_type)
                each_fee = st.operation_fee * item.amount
            except:
                pass
            fee += each_fee
        return fee

    def can_merge(self):
        orders = Order.objects.filter(company=self.company, status='1')
        text = '合并提示：<br>'
        sum = 0
        for item in orders:
            if item.id != self.id:
                if  self.user_id == item.user_id and self.buyer_full_name == item.buyer_full_name and \
                    self.buyer_phone_number == item.buyer_phone_number and self.buyer_email == item.buyer_email and \
                    self.buyer_postcode == item.buyer_postcode and self.buyer_city == item.buyer_city and \
                    self.buyer_county == item.buyer_county and self.buyer_country == item.buyer_country and \
                    self.buyer_address1 == item.buyer_address1 and self.buyer_address2 == item.buyer_address2 :
                    msg = '本记录可与id为' + str(item.id) + '的记录进行B类合并<br>'
                    sum += 1
                    if self.sales_record_number == item.sales_record_number:
                        msg = '本记录可与id为' + str(item.id) + '的记录进行A类合并<br>'
                    text += msg
        if sum == 0:
            return False
        else:
            return text

class Ordercontain(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单编号')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, null=True, verbose_name='SKU名称')
    amount = models.PositiveSmallIntegerField(verbose_name='数量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Ordercomment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    content = models.TextField('评论内容')
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    class Meta:
        verbose_name = '订单评论'
        verbose_name_plural = verbose_name

class Reject(models.Model):
    STATUS = (
        ('1','退件接收'),
        ('2','完结')
    )
    company = models.ForeignKey(Company, verbose_name='所属公司', on_delete=models.SET_NULL, blank=False, null=True)
    depot = models.ForeignKey(Depot, verbose_name='接受退件的仓库', null=True, default=None, blank=True, on_delete=models.SET_NULL)
    reject_code = models.CharField(max_length=24, verbose_name='退件仓库单号', blank=True, default='')
    sales_record_number = models.CharField(max_length=50, verbose_name='客户销售平台订单号', blank=True, default='')
    user_id = models.CharField(max_length=80, verbose_name='客户平台消费者id', blank=True, default='')
    buyer_full_name = models.CharField(max_length=30, verbose_name='消费者姓名', blank=True, default='')
    buyer_phone_number = models.CharField(max_length=20, verbose_name='消费者联系电话', blank=True, default='')
    buyer_email = models.EmailField(max_length=100, verbose_name='消费者电子邮箱', blank=True, default='')
    buyer_address1 = models.CharField(max_length=100, verbose_name='消费者地址1', blank=True, default='')
    buyer_address2 = models.CharField(max_length=100, verbose_name='消费者地址2', blank=True, default='')
    buyer_city = models.CharField(max_length=20, verbose_name='City/Town', blank=True, default='')
    buyer_county = models.CharField(max_length=20, verbose_name='County', blank=True, default='')
    buyer_country = models.CharField(max_length=20, verbose_name='Country', blank=True, default='')
    buyer_postcode = models.CharField(max_length=10, verbose_name='消费者邮编', blank=True, default='')
    status = models.CharField(choices=STATUS, max_length=1, verbose_name='订单状态', blank=True, default='1')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='退件接受时间')
    over_time = models.DateTimeField(auto_now=True, verbose_name="退件完结时间")
    stock_time = models.CharField(max_length=50, verbose_name='退单储存时间', blank=True, default='')
    stock_fee = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="退单仓储费",blank=True, default=0)
    delivery_service = models.CharField(max_length=30, verbose_name='退件物流服务', default='', blank=True)
    delivery_code = models.CharField(max_length=30, verbose_name='退件物流单号', default='', blank=True)
    # final_weight = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='退件重量', blank=True, default=0)
    # final_delivery_fee = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='退件体积', blank=True, default=0)
    custom_lable = models.ManyToManyField(Sku, through='Rejectcontain')
    remarks = models.TextField(verbose_name='操作记录', blank=True, default='')

    def __str__(self):
        return self.reject_code

    def __repr__(self):
        return self.reject_code

    class Meta:
        verbose_name = '退件'
        verbose_name_plural = verbose_name


    def total_weight(self):
        skus = self.rejectcontain_set.all()
        total_weight = 0
        fee = 0
        for item in skus:
            each_weight = item.sku.weight * item.amount
            total_weight += each_weight
        return total_weight


    def total_volume(self):
        skus = self.rejectcontain_set.all()
        total_volume = 0
        fee = 0
        for item in skus:
            each_volume = item.sku.volume * item.amount
            total_volume += each_volume
        return total_volume


    def count_reject_stock_time(self):
        #计算退件进入仓库的时间，退单处理完成后，该数值要记录
        # create_time = self.create_time.replace(tzinfo=None)
        exist_time = timezone.now() - self.create_time
        return exist_time


    def count_reject_stock_fee(self):
        #计算退件仓储费，退件处理完毕后，要扣除费用，记录数值
        exist = self.count_reject_stock_time()
        exist_days =  int(exist.days)
        if exist_days > 20:
            fee = (exist_days - 20) * 0.5
        else:
            fee = 0
        return fee

    @classmethod
    def create_reject_code(self):
        import random
        d = timezone.now()
        prefix = d.strftime("%y%m%d")
        tail = random.randrange(100, 999)
        return 'TJ'+prefix + str(tail)


class Rejectcontain(models.Model):
    reject = models.ForeignKey(Reject, on_delete=models.CASCADE, verbose_name='推荐单号')
    sku = models.ForeignKey(Sku, on_delete=models.SET_NULL, null=True, verbose_name='退件SKU')
    amount = models.PositiveIntegerField(verbose_name='退件数量')
    create_time = models.DateTimeField(auto_now_add=True)


class Orderspecial(models.Model):
    postcode = models.CharField(max_length=10, verbose_name='邮编', blank=False, unique=True, default='')

    class Meta:
        verbose_name = '特殊地区邮编'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.postcode

    def __repr__(self):
        return self.postcode

    @classmethod
    def all_special_postcode(self):
        all_query_set = Orderspecial.objects.all()
        postcode_list = []
        for item in all_query_set:
            postcode_list.append(item.postcode)
        return postcode_list


# class Orderdelivery(models.Model):
#     order = models.ForeignKey(Order, verbose_name='订单号')
#     delivery = models.ForeignKey(Delivery, verbose_name='物流方案')
#     code = models.CharField(max_length=30, verbose_name='物流单号')
#     fee_auto = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='自动核算运费')
#     fee_confirm = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='最终确认运费')
#
#     class Meta:
#         verbose_name = '订单物流方案'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         self.delivery.__str__()
#
#     def __repr__(self):
#         self.delivery.__repr__()



