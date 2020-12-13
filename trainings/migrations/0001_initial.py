# Generated by Django 3.1 on 2020-12-01 22:40

import autoslug.fields
from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_text', models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание')),
                ('meta_description', models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)')),
                ('text', models.TextField(verbose_name='Контент')),
                ('title', models.CharField(max_length=500, verbose_name='Название тренинга')),
                ('url', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True, verbose_name='URL тренинга')),
                ('active', models.BooleanField(default=True, help_text='Неактивные тренинги не будут отображаться на сайте', verbose_name='Активно')),
                ('image', models.ImageField(blank=True, help_text='Возможность обрезки появится после сохранения', null=True, upload_to='', verbose_name='Изображение')),
                ('sidebar_size', image_cropping.fields.ImageRatioField('image', '140x140', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='Обрезка изображения для превью (сайдбар)')),
                ('thumbnail_size', image_cropping.fields.ImageRatioField('image', '512x288', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='Обрезка изображения для превью (список тренингов)')),
                ('location', models.CharField(max_length=500, verbose_name='Место проведения тренинга')),
                ('date_arranged', models.DateTimeField(blank=True, help_text='При отсутсвии даты будет отображено "Скоро"', null=True, verbose_name='Дата и время проведения тренинга')),
                ('sorting', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения в списках')),
            ],
            options={
                'verbose_name': 'Тренинг',
                'verbose_name_plural': 'Тренинги',
                'ordering': ['sorting'],
            },
        ),
    ]
