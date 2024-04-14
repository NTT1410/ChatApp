# Generated by Django 5.0.4 on 2024-04-14 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat', '0004_alter_connection_active_alter_group_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='connection',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]