# Generated by Django 4.1.5 on 2023-04-03 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reuniones', '0008_delete_roledelegado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='callable_roles',
        ),
        migrations.AddField(
            model_name='role',
            name='callable_roles',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='reuniones.role'),
        ),
    ]