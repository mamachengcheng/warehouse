# Generated by Django 2.0 on 2018-05-28 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20180213_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_service',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Delivery', verbose_name='物流服务'),
        ),
    ]
