# Generated by Django 5.1.4 on 2025-01-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcompletereport',
            name='description',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='taskincompletereport',
            name='description',
            field=models.TextField(unique=True),
        ),
    ]