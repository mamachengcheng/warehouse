# Generated by Django 2.0 on 2018-01-07 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20180101_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercontain',
            name='sku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='depot.Sku', verbose_name='SKU名称'),
        ),
    ]