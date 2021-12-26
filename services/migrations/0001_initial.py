# Generated by Django 3.1.4 on 2021-12-20 01:28

import autoslug.fields
from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_text', models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание')),
                ('short_text_ru', models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание')),
                ('short_text_uz', models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание')),
                ('meta_description', models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)')),
                ('meta_description_ru', models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)')),
                ('meta_description_uz', models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)')),
                ('text', models.TextField(verbose_name='Контент')),
                ('text_ru', models.TextField(null=True, verbose_name='Контент')),
                ('text_uz', models.TextField(null=True, verbose_name='Контент')),
                ('title', models.CharField(max_length=500, verbose_name='Название услуги')),
                ('title_ru', models.CharField(max_length=500, null=True, verbose_name='Название услуги')),
                ('title_uz', models.CharField(max_length=500, null=True, verbose_name='Название услуги')),
                ('url', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True, verbose_name='URL услуги')),
                ('active', models.BooleanField(default=True, help_text='Неактивные услуги не будут отображаться на сайте', verbose_name='Активно')),
                ('image', models.ImageField(blank=True, help_text='Возможность обрезки появится после сохранения', null=True, upload_to='trainings/', verbose_name='Изображение')),
                ('thumbnail_size', image_cropping.fields.ImageRatioField('image', '512x288', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='Обрезка изображения для превью (список услуг)')),
                ('sidebar_size', image_cropping.fields.ImageRatioField('image', '140x140', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='Обрезка изображения для превью (сайдбар)')),
                ('price', models.IntegerField(verbose_name='Цена на услугу')),
                ('special_price', models.IntegerField(verbose_name='Специальная цена на услугу')),
                ('sorting', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения в списках')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['sorting'],
            },
        ),
    ]
