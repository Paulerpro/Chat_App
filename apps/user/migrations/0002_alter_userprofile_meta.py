# Generated by Django 4.2 on 2024-10-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='meta',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]