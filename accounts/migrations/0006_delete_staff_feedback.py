# Generated by Django 3.2.12 on 2022-03-11 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_staff_feedback_feedback_reply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Staff_Feedback',
        ),
    ]
