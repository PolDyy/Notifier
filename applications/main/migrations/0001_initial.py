# Generated by Django 4.2.5 on 2023-09-13 16:45

import applications.core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(blank=True, max_length=200, verbose_name='Название сайта')),
                ('site_description', models.TextField(blank=True, verbose_name='Описание сайта')),
                ('site_photo', models.ImageField(blank=True, help_text='Загружать JPG с размерами 1200x630px', upload_to=applications.core.models.PathAndRename('main/preference/site_photo'), verbose_name='Фотография сайта')),
                ('header_html', models.TextField(blank=True, help_text='Вставка html-кода для всех страниц сайта перед закрывающимся тегом HEAD', verbose_name='HEAD')),
                ('footer_html', models.TextField(blank=True, help_text='Вставка html-кода для всех страниц сайта перед закрывающимся тегом FOOTER', verbose_name='FOOTER')),
            ],
            options={
                'verbose_name': 'настройки',
                'verbose_name_plural': 'настройки',
            },
        ),
    ]
