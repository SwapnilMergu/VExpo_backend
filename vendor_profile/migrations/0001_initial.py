# Generated by Django 5.0.4 on 2024-04-17 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('address', models.TextField(default='')),
                ('profile', models.TextField(default='')),
                ('DOB', models.TextField(default='')),
                ('whatsapp_no', models.TextField(default='')),
                ('social_links', models.TextField(default='')),
                ('status', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_profile.adminprofile')),
            ],
            options={
                'db_table': 'vendor_profile',
            },
        ),
    ]