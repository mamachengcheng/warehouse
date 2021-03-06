# Generated by Django 2.0 on 2017-12-18 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nickname',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='account',
            name='company',
            field=models.ForeignKey(blank=True, help_text='请指定该账户属于哪个公司。注意！请不要指定一个用户是仓库管理员的同时还属于某个公司！', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='请选择该账户是否属于仓库管理员。注意！请不要指定一个用户是仓库管理员的同时还属于某个公司！', max_length=10, verbose_name='是否仓库管理员'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '保存'), (2, '发布'), (3, '撤回')], default=1, verbose_name='公告状态'),
        ),
        migrations.AlterField(
            model_name='company',
            name='prepayment',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='预存款'),
        ),
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(help_text='名称必须唯一，且不能超过20个字符，可以使用中文、英文或数字的组合', max_length=20, unique=True, verbose_name='公司等级'),
        ),
    ]
