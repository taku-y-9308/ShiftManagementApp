# Generated by Django 3.2.12 on 2022-10-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftManagementApp', '0021_shift_archive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField(verbose_name='shop_id')),
                ('deadline', models.IntegerField(verbose_name='deadline')),
            ],
        ),
    ]
