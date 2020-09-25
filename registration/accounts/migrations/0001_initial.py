# Generated by Django 3.0 on 2020-09-25 21:41

import accounts.manager
from django.db import migrations, models
import django.utils.crypto
import django.utils.timezone
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=130, unique=True, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('phone', models.CharField(error_messages={'unique': 'Another user with this phone number already exists'}, max_length=16, unique=True, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email')),
                ('is_send_letter', models.BooleanField(default=False, verbose_name='letter is send')),
                ('token', models.CharField(default=functools.partial(django.utils.crypto.get_random_string, *(64,), **{}), max_length=64)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('username',),
            },
            managers=[
                ('objects', accounts.manager.UserManager()),
            ],
        ),
    ]
