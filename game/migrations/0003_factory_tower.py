# Generated by Django 2.0.3 on 2018-03-15 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_support'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('price', models.IntegerField()),
                ('img', models.ImageField(upload_to='factories')),
                ('tower_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('oil', models.IntegerField()),
                ('price', models.IntegerField()),
                ('img', models.ImageField(upload_to='towers')),
            ],
        ),
    ]