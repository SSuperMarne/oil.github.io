# Generated by Django 2.0.3 on 2018-03-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=128)),
                ('text', models.TextField(max_length=2048)),
            ],
        ),
    ]