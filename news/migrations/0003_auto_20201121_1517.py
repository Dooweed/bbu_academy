# Generated by Django 3.1 on 2020-11-21 10:17

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20201120_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='article_size',
        ),
        migrations.AlterField(
            model_name='article',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Оставьте поле пустым, чтобы использовать первые 250 знаков статьи', max_length=1000, null=True, verbose_name='Описание (мета-тег)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('editing', 'Редактирование'), ('pending', 'Ожидание'), ('published', 'Опубликовано')], default='editing', help_text='Отображаться будут только статьи с состоянием "Опубликовано"', max_length=30, verbose_name='Состояние статьи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail_size',
            field=image_cropping.fields.ImageRatioField('image', '1024x576', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Обрезка изображения для превью'),
        ),
    ]
