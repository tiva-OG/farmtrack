# Generated by Django 5.1.7 on 2025-04-10 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_shortenedlink_short_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedlink',
            name='short_code',
            field=models.CharField(default='01372f', max_length=10, unique=True),
        ),
    ]
