# Generated by Django 3.2.12 on 2022-03-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftManagementApp', '0002_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='begin',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='shift',
            name='date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='shift',
            name='finish',
            field=models.CharField(max_length=10),
        ),
    ]
