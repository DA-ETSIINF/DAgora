# Generated by Django 4.1.5 on 2023-08-13 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_profiles', '0005_remove_role_callable_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='show_email',
            field=models.BooleanField(default=True),
        ),
    ]
