# Generated by Django 5.0.4 on 2024-04-17 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stalls', '0001_initial'),
        ('visitors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(blank=True, default=None, null=True)),
                ('review', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stalls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stalls.stalls')),
                ('visitors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitors.visitors')),
            ],
            options={
                'db_table': 'visits',
            },
        ),
    ]