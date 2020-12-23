# Generated by Django 3.1.4 on 2020-12-21 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0005_auto_20201221_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='meta_description_ru',
            field=models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)'),
        ),
        migrations.AddField(
            model_name='training',
            name='meta_description_uz',
            field=models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=250, null=True, verbose_name='Описание (мета-тег)'),
        ),
        migrations.AddField(
            model_name='training',
            name='short_text_ru',
            field=models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='training',
            name='short_text_uz',
            field=models.CharField(blank=True, help_text='Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые 500 знаков статьи', max_length=500, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='training',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='Контент'),
        ),
        migrations.AddField(
            model_name='training',
            name='text_uz',
            field=models.TextField(null=True, verbose_name='Контент'),
        ),
        migrations.AddField(
            model_name='training',
            name='title_ru',
            field=models.CharField(max_length=500, null=True, verbose_name='Название тренинга'),
        ),
        migrations.AddField(
            model_name='training',
            name='title_uz',
            field=models.CharField(max_length=500, null=True, verbose_name='Название тренинга'),
        ),
    ]
