# Generated by Django 3.2.12 on 2022-05-17 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftManagementApp', '0014_line_user_id_nonce'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line_user_id',
            old_name='user_id',
            new_name='user',
        ),
    ]