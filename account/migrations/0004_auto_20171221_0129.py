# Generated by Django 2.0 on 2017-12-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20171220_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='action',
            field=models.CharField(choices=[('0', '其他'), ('1', '新建'), ('2', '删除'), ('3', '修改'), ('4', '查询'), ('5', '审核SKU'), ('6', '提交到货预报'), ('7', '审核到货预报'), ('8', '入库')], max_length=8, verbose_name='动作'),
        ),
    ]
