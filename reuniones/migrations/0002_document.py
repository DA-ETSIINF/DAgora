# Generated by Django 4.0 on 2023-02-22 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuniones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='documents/')),
            ],
        ),
    ]
