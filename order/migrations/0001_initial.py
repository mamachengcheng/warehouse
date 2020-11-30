# Generated by Django 2.0 on 2017-12-15 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('depot', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='物流中文名称-CN')),
                ('name_en', models.CharField(blank=True, default='', max_length=40, verbose_name='物流英文名称-EN')),
                ('instruction', models.CharField(blank=True, default=0, max_length=100, verbose_name='备注')),
                ('one', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.000-0.020')),
                ('two', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.021-0.050')),
                ('three', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.051-0.100')),
                ('four', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.101-0.250')),
                ('five', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.251-0.500')),
                ('six', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.501-0.750')),
                ('seven', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='0.751-1.000')),
                ('eight', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='1.001-2.000')),
                ('nine', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='2.001-3.000')),
                ('ten', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='3.001-4.000')),
                ('eleven', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='4.001-5.000')),
                ('twelve', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='5.001-6.000')),
                ('thirteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='6.001-7.000')),
                ('fourteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='7.001-8.000')),
                ('fifiteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='8.001-9.000')),
                ('sixteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='9.001-10.000')),
                ('seventeen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='10.001-11.000')),
                ('eighteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='11.001-12.000')),
                ('nineteen', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='12.001-13.000')),
                ('twenty', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='13.001-14.000')),
                ('twenty_one', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='14.001-15.000')),
                ('twenty_two', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='15.001-16.000')),
                ('twenty_three', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='16.001-17.000')),
                ('twenty_four', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='17.001-18.000')),
                ('twenty_five', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='18.001-19.000')),
                ('twenty_six', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='19.001-20.000')),
                ('twenty_seven', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='20.001-21.000')),
                ('twenty_eight', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='21.001-22.000')),
                ('twenty_nine', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='22.001-23.000')),
                ('thirty', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='23.001-24.000')),
                ('thirty_one', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='24.001-25.000')),
                ('thirty_two', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='25.001-26.000')),
                ('thirty_three', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='26.001-27.000')),
                ('thirty_four', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='27.001-28.000')),
                ('thirty_five', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='28.001-29.000')),
                ('thirty_six', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='29.001-30.000')),
                ('thirty_seven', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='此处为30KG以上的货物运费计算方式，在29.001-30.000的基础上，每公斤增加的运费，小数位向上取整', max_digits=5, verbose_name='30.001-')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Level', verbose_name='所属客户等级')),
            ],
            options={
                'verbose_name': '物流运费',
                'verbose_name_plural': '物流运费',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_record_number', models.CharField(max_length=50, verbose_name='客户销售平台订单号')),
                ('user_id', models.CharField(blank=True, default='', max_length=80, verbose_name='客户平台消费者id')),
                ('buyer_full_name', models.CharField(max_length=30, verbose_name='消费者姓名')),
                ('buyer_phone_number', models.CharField(max_length=20, verbose_name='消费者联系电话')),
                ('buyer_email', models.EmailField(blank=True, default='', max_length=100, verbose_name='消费者电子邮箱')),
                ('buyer_address1', models.CharField(max_length=100, verbose_name='消费者地址1')),
                ('buyer_address2', models.CharField(blank=True, default='', max_length=100, verbose_name='消费者地址2')),
                ('buyer_city', models.CharField(max_length=20, verbose_name='City/Town')),
                ('buyer_county', models.CharField(default='', max_length=20, verbose_name='County')),
                ('buyer_country', models.CharField(max_length=20, verbose_name='Country')),
                ('buyer_postcode', models.CharField(max_length=10, verbose_name='消费者邮编')),
                ('status', models.CharField(blank=True, choices=[('1', '未提交'), ('2', '已提交'), ('3', '已处理'), ('4', '已出库'), ('5', '已完结'), ('6', '问题单'), ('7', '其他')], default='1', max_length=1, verbose_name='订单状态')),
                ('order_code', models.CharField(blank=True, default='', max_length=24, verbose_name='订单编号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('delivery_code', models.CharField(default='', max_length=30, verbose_name='物流单号')),
                ('final_weight', models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='最终重量')),
                ('final_delivery_fee', models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='最终运费')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
        migrations.CreateModel(
            name='Ordercomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('comment_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
            options={
                'verbose_name': '订单评论',
                'verbose_name_plural': '订单评论',
            },
        ),
        migrations.CreateModel(
            name='Ordercontain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Sku')),
            ],
        ),
        migrations.CreateModel(
            name='Reject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(blank=True, default='', max_length=24, verbose_name='退件仓库单号')),
                ('sales_record_number', models.CharField(blank=True, default='', max_length=50, verbose_name='客户销售平台订单号')),
                ('user_id', models.CharField(blank=True, default='', max_length=80, verbose_name='客户平台消费者id')),
                ('buyer_full_name', models.CharField(blank=True, default='', max_length=30, verbose_name='消费者姓名')),
                ('buyer_phone_number', models.CharField(blank=True, default='', max_length=20, verbose_name='消费者联系电话')),
                ('buyer_email', models.EmailField(blank=True, default='', max_length=100, verbose_name='消费者电子邮箱')),
                ('buyer_address1', models.CharField(blank=True, default='', max_length=100, verbose_name='消费者地址1')),
                ('buyer_address2', models.CharField(blank=True, default='', max_length=100, verbose_name='消费者地址2')),
                ('buyer_city', models.CharField(blank=True, default='', max_length=20, verbose_name='City/Town')),
                ('buyer_county', models.CharField(blank=True, default='', max_length=20, verbose_name='County')),
                ('buyer_country', models.CharField(blank=True, default='', max_length=20, verbose_name='Country')),
                ('buyer_postcode', models.CharField(blank=True, default='', max_length=10, verbose_name='消费者邮编')),
                ('status', models.CharField(blank=True, choices=[('1', '退件接受'), ('2', '完结')], default='1', max_length=1, verbose_name='订单状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='退件接受时间')),
                ('delivery_service', models.CharField(blank=True, default='', max_length=30, verbose_name='退件物流服务')),
                ('delivery_code', models.CharField(blank=True, default='', max_length=30, verbose_name='退件物流单号')),
                ('final_weight', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, verbose_name='退件重量')),
                ('final_delivery_fee', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, verbose_name='退件体积')),
                ('remarks', models.TextField(blank=True, default='', verbose_name='操作记录')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '退件',
                'verbose_name_plural': '退件',
            },
        ),
        migrations.CreateModel(
            name='Rejectcontain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('reject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Reject')),
                ('sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Sku')),
            ],
        ),
        migrations.AddField(
            model_name='reject',
            name='custom_lable',
            field=models.ManyToManyField(through='order.Rejectcontain', to='depot.Sku'),
        ),
        migrations.AddField(
            model_name='reject',
            name='depot',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Depot', verbose_name='接受退件的仓库'),
        ),
        migrations.AddField(
            model_name='order',
            name='custom_lable',
            field=models.ManyToManyField(through='order.Ordercontain', to='depot.Sku'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_service',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Delivery', verbose_name='物流服务'),
        ),
        migrations.AddField(
            model_name='order',
            name='depot',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Depot', verbose_name='出货仓库'),
        ),
    ]
