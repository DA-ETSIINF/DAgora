# Generated by Django 4.0 on 2023-08-17 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reunion_system', '0003_meeting_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date',
        ),
    ]