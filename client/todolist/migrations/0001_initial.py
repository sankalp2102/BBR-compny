# Generated by Django 5.1.4 on 2025-02-02 04:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonAttendaceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('Number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlantAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('Number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCompleteReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(unique=True)),
                ('shift', models.IntegerField(choices=[(1, 'Shift 1'), (2, 'Shift 2')])),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskIncompleteReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(unique=True)),
                ('reason', models.TextField()),
                ('photo', models.ImageField(upload_to='uploads')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('shift', models.IntegerField(choices=[(1, 'Shift 1'), (2, 'Shift 2')])),
                ('date', models.DateField()),
                ('machines', models.TextField()),
                ('people', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.site')),
            ],
            options={
                'ordering': ['-date', 'shift'],
            },
        ),
        migrations.AddField(
            model_name='site',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.state'),
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together={('name', 'state')},
        ),
    ]
