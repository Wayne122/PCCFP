# Generated by Django 2.0 on 2017-12-30 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20171230_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='read_by',
            field=models.ManyToManyField(blank=True, related_name='read_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
