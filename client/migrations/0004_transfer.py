# Generated by Django 2.0.3 on 2018-03-15 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20180315_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('system', models.CharField(max_length=16)),
                ('vault', models.CharField(max_length=64)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
        ),
    ]
