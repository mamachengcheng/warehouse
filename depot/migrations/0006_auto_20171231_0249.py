# Generated by Django 2.0 on 2017-12-30 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depot', '0005_auto_20171223_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerlevelfee',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Level', unique=True, verbose_name='客户等级'),
        ),
    ]
