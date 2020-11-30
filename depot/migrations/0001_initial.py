# Generated by Django 2.0 on 2017-12-15 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal', models.IntegerField(blank=True, default=0, verbose_name='正常')),
                ('preparing_in', models.IntegerField(blank=True, default=0, verbose_name='待入库')),
                ('preparing_out', models.IntegerField(blank=True, default=0, verbose_name='待出库')),
                ('freeze', models.IntegerField(blank=True, default=0, verbose_name='冻结')),
                ('short', models.IntegerField(blank=True, default=0, verbose_name='缺货')),
                ('other', models.IntegerField(blank=True, default=0, verbose_name='其他')),
            ],
            options={
                'verbose_name': 'SKU数量',
                'verbose_name_plural': 'SKU数量',
            },
        ),
        migrations.CreateModel(
            name='Customerlevelfee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reject_check_fee', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='退件接收检查费')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Level', verbose_name='客户等级')),
            ],
        ),
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': '仓库不能重名，您输入的仓库名称已经存在了，请换一个名字。'}, max_length=150, unique=True, verbose_name='仓库名称')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='仓库地址')),
            ],
            options={
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库',
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('check', models.IntegerField()),
            ],
            options={
                'verbose_name': '货物数量预报',
            },
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='SKU名称-中文')),
                ('name_en', models.CharField(blank=True, default='', max_length=50, verbose_name='SKU名称-英文')),
                ('code', models.CharField(default='', max_length=50, verbose_name='产品代码')),
                ('status', models.CharField(choices=[('0', '待审核'), ('1', '已审核')], default=0, max_length=12, verbose_name='Sku状态')),
                ('declare_code', models.CharField(blank=True, default='', max_length=50, verbose_name='海关申报代码')),
                ('price', models.CharField(blank=True, default='', max_length=20, verbose_name='申报价值')),
                ('img', models.ImageField(blank=True, upload_to='img', verbose_name='图片')),
                ('weight', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=6, verbose_name='重量')),
                ('volume', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='体积')),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': 'SKU信息',
                'verbose_name_plural': 'SKU信息',
            },
        ),
        migrations.CreateModel(
            name='Skutype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'SKU类别不能重名，请重新输入SKU类别名称'}, max_length=20, unique=True, verbose_name='SKU类别')),
            ],
            options={
                'verbose_name': 'SKU类别',
                'verbose_name_plural': 'SKU类别',
            },
        ),
        migrations.CreateModel(
            name='Skutypefee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_fee', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='操作费')),
                ('in_fee', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='入仓费')),
                ('level', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Level')),
                ('skutype', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='depot.Skutype')),
            ],
            options={
                'verbose_name': 'Sku类别费用',
                'verbose_name_plural': 'Sku类别费用',
            },
        ),
        migrations.CreateModel(
            name='Transorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_arrive', models.DateField(verbose_name='预计到达时间')),
                ('transport_code', models.CharField(blank=True, default='', max_length=50, verbose_name='货运单号')),
                ('transport_firm', models.CharField(blank=True, default='', max_length=50, verbose_name='货运公司')),
                ('value_all', models.CharField(blank=True, default='', max_length=10, verbose_name='货值总计')),
                ('remark', models.TextField(blank=True, default='', max_length=300, verbose_name='备注')),
                ('status_trans', models.CharField(choices=[('1', '未提交'), ('2', '已提交'), ('3', '已验收'), ('4', '完结')], default='1', max_length=2, verbose_name='运单状态')),
                ('check', models.TextField(blank=True, default='', verbose_name='核对说明')),
                ('date_check', models.DateTimeField(auto_now=True, verbose_name='验收时间')),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司')),
                ('depot', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Depot', verbose_name='目标仓库')),
                ('skus', models.ManyToManyField(through='depot.Prediction', to='depot.Sku', verbose_name='包含货物')),
            ],
            options={
                'verbose_name': '预计到货订单',
                'verbose_name_plural': '预计到货订单',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='库位编号')),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depot.Depot', verbose_name='所属仓库')),
            ],
            options={
                'verbose_name': '库位',
                'verbose_name_plural': '库位',
            },
        ),
        migrations.AddField(
            model_name='sku',
            name='skutype',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Skutype', verbose_name='SKU类别'),
        ),
        migrations.AddField(
            model_name='sku',
            name='unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Unit'),
        ),
        migrations.AddField(
            model_name='prediction',
            name='sku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Sku'),
        ),
        migrations.AddField(
            model_name='prediction',
            name='transorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depot.Transorder'),
        ),
        migrations.AddField(
            model_name='count',
            name='depot',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Depot'),
        ),
        migrations.AddField(
            model_name='count',
            name='sku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='depot.Sku'),
        ),
    ]