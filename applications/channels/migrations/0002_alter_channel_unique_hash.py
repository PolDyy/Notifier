# Generated by Django 4.2.5 on 2023-09-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='unique_hash',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]