# Generated by Django 3.2.12 on 2022-03-16 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_student_leave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.session_year')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.student')),
            ],
        ),
    ]
