# Generated by Django 4.0 on 2023-08-17 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reunion_system', '0002_remove_meeting_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
