# Generated by Django 2.0 on 2018-01-01 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20171223_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prepayrecord',
            name='instruction',
            field=models.CharField(blank=True, default='', help_text='请输入费用发生的详细原因，便于后期记录查找', max_length=100, verbose_name='说明'),
        ),
    ]
