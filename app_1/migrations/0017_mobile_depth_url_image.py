# Generated by Django 4.1.4 on 2023-02-21 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0016_browsing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile_depth',
            name='url_image',
            field=models.CharField(default='image', max_length=900),
        ),
    ]
