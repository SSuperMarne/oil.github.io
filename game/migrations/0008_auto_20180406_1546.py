# Generated by Django 2.0.3 on 2018-04-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20180406_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factory',
            name='img',
            field=models.ImageField(help_text='Изображение завода', upload_to='factories'),
        ),
    ]
