# Generated by Django 4.0 on 2023-07-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reunion_system', '0004_file_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]