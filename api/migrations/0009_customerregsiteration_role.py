# Generated by Django 3.1.3 on 2021-02-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210224_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerregsiteration',
            name='role',
            field=models.CharField(default='Customer', max_length=10),
        ),
    ]
