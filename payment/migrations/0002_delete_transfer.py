# Generated by Django 2.0.3 on 2018-03-15 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transfer',
        ),
    ]