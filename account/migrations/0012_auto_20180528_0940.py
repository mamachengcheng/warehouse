# Generated by Django 2.0 on 2018-05-28 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20180210_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='action',
            field=models.CharField(choices=[('0', '其他'), ('1', '新建'), ('2', '删除'), ('3', '修改'), ('4', '查询'), ('5', '审核SKU'), ('6', '提交到货预报'), ('7', '审核到货预报'), ('8', '入库'), ('9', '出库'), ('10', '手动修改库存'), ('11', '订单完结'), ('12', '取消订单')], max_length=8, verbose_name='动作'),
        ),
    ]
