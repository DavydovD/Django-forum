# Generated by Django 2.1.5 on 2019-02-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20190202_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='description',
            field=models.CharField(default='some description', max_length=255),
        ),
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.CharField(default='some description', max_length=255),
        ),
    ]
