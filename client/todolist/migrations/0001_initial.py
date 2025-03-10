# Generated by Django 5.1.4 on 2025-03-10 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machinery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shift', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personnel_engaged', models.JSONField(default=list)),
                ('machinery_used', models.JSONField(default=list)),
                ('equipment_used', models.JSONField(default=list)),
                ('personnel_idled', models.JSONField(blank=True, default=list, null=True)),
                ('equipment_idled', models.JSONField(blank=True, default=list, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personnel_list', models.JSONField(default=list)),
                ('date', models.DateField()),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.shift')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.site')),
            ],
        ),
        migrations.AddField(
            model_name='shift',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.site'),
        ),
        migrations.AddField(
            model_name='site',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.state'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('machinery', models.ManyToManyField(related_name='tasks', to='todolist.machinery')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.shift')),
            ],
        ),
        migrations.CreateModel(
            name='ReasonForDelay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('time_reported', models.DateTimeField(auto_now_add=True)),
                ('task_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.taskreport')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Partially Complete', 'Partially Complete')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.task')),
            ],
        ),
        migrations.AddField(
            model_name='taskreport',
            name='task_status',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='todolist.taskstatus'),
        ),
    ]
