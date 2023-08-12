# Generated by Django 4.1.5 on 2023-07-20 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_profiles', '0002_group_permission_role_group_role_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='groups',
            field=models.ManyToManyField(to='custom_profiles.group'),
        ),
        migrations.AlterField(
            model_name='role',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='custom_profiles.group'),
        ),
    ]
