# Generated by Django 5.1.7 on 2025-04-08 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_user_init_fish_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='livestock_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='short_code',
            field=models.CharField(default='9749f8', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='farm_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
