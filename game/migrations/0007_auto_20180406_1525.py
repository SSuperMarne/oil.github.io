# Generated by Django 2.0.3 on 2018-04-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20180328_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factory',
            name='img',
            field=models.FileField(help_text='Изображение завода', upload_to='factories'),
        ),
    ]
