# Generated by Django 4.1.4 on 2023-02-06 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_staff',
        ),
    ]
