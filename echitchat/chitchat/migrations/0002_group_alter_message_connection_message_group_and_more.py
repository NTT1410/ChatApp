# Generated by Django 5.0.4 on 2024-04-11 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='message',
            name='connection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chitchat.connection'),
        ),
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chitchat.group'),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='chitchat.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('group', 'user')},
            },
        ),
    ]
