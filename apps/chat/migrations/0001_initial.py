# Generated by Django 4.2 on 2024-10-19 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('DELETED', 'DELETED')], default='ACTIVE', max_length=100)),
                ('meta', models.JSONField(blank=True, default=dict, null=True)),
                ('group_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('DELETED', 'DELETED')], default='ACTIVE', max_length=100)),
                ('meta', models.JSONField(blank=True, default=dict, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_messages', to='chat.chatgroup')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
