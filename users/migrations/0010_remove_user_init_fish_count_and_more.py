# Generated by Django 5.1.7 on 2025-04-08 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_shortenedlink_short_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='init_fish_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='init_poultry_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='livestock_type',
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='short_code',
            field=models.CharField(default='953564', max_length=10, unique=True),
        ),
    ]
