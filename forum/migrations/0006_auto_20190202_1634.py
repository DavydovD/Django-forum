# Generated by Django 2.1.5 on 2019-02-02 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20190202_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='profile',
        ),
    ]
