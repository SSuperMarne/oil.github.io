# Generated by Django 2.0.3 on 2018-03-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20180315_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stat_payout',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='stat_produced',
            field=models.IntegerField(default=0),
        ),
    ]