# Generated by Django 2.0.3 on 2018-03-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20180320_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tower',
            name='oil',
            field=models.IntegerField(help_text='Производительность нефти в 24 часа (укажите число)'),
        ),
    ]
