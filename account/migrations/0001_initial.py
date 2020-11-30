# Generated by Django 2.0 on 2017-12-15 16:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, help_text='请选择该账户是否属于仓库管理员', max_length=10, verbose_name='是否仓库管理员')),
                ('phone', models.CharField(blank=True, default='', max_length=30, verbose_name='电话号码')),
            ],
            options={
                'verbose_name': '账户',
                'verbose_name_plural': '账户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='公告标题')),
                ('summary', models.CharField(max_length=200, verbose_name='简介')),
                ('content', models.TextField(verbose_name='公告内容')),
                ('publish_time', models.DateTimeField(auto_now=True, verbose_name='发布时间')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, '保存'), (2, '发布'), (3, '撤回')], default=1)),
                ('account', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='发布人')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='公司名称')),
                ('address', models.CharField(blank=True, default='', max_length=200, verbose_name='公司地址')),
                ('contacts', models.CharField(blank=True, default='', max_length=20, verbose_name='联系人')),
                ('contacts_phone', models.CharField(blank=True, default='', max_length=20, verbose_name='联系电话')),
                ('prepayment', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='预存款')),
            ],
            options={
                'verbose_name': '公司',
                'verbose_name_plural': '公司',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='公司等级')),
            ],
            options={
                'verbose_name': '公司等级',
                'verbose_name_plural': '公司等级',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('0', '其他'), ('1', '新建'), ('2', '删除'), ('3', '修改'), ('4', '查询')], max_length=8, verbose_name='动作')),
                ('description', models.CharField(blank=True, default='', max_length=200, verbose_name='描述')),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(blank=True, default='', max_length=200)),
                ('action_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作者')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '操作记录',
                'verbose_name_plural': '操作记录',
            },
        ),
        migrations.CreateModel(
            name='Prepayrecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='金额')),
                ('instruction', models.CharField(blank=True, default='', max_length=30, verbose_name='说明')),
                ('type', models.SmallIntegerField(choices=[(1, '预存款'), (2, '入仓费'), (3, '操作费'), (4, '订单运费'), (5, '仓租'), (6, '退件接受检查费'), (7, '其他')], verbose_name='费用类别')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='触发时间')),
                ('account', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company')),
            ],
            options={
                'verbose_name': '费用记录',
                'verbose_name_plural': '费用记录',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='level',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Level', verbose_name='公司等级'),
        ),
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Company', verbose_name='所属公司'),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]