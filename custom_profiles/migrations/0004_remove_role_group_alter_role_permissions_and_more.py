# Generated by Django 4.1.5 on 2023-07-20 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_profiles', '0003_permission_groups_alter_role_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='group',
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='roles', to='custom_profiles.permission'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.ManyToManyField(blank=True, to='custom_profiles.role'),
        ),
        migrations.AddField(
            model_name='role',
            name='group',
            field=models.ManyToManyField(to='custom_profiles.group'),
        ),
    ]
