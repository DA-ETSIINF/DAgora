# Generated by Django 4.0 on 2023-07-14 20:23

from django.db import migrations, models
import reunion_system.models


class Migration(migrations.Migration):

    dependencies = [
        ('reunion_system', '0002_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(max_length=300, upload_to=reunion_system.models.get_file_upload_path),
        ),
    ]
