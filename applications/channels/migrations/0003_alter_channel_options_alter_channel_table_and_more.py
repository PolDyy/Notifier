# Generated by Django 4.2.5 on 2023-09-20 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0002_alter_channel_unique_hash'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={},
        ),
        migrations.AlterModelTable(
            name='channel',
            table='channels',
        ),
        migrations.AlterModelTable(
            name='message',
            table='messages',
        ),
    ]
