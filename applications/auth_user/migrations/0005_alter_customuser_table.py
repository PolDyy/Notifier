# Generated by Django 4.2.5 on 2023-09-20 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='custom_user',
        ),
    ]
