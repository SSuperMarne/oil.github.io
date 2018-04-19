# Generated by Django 2.0.3 on 2018-04-19 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurfingSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('title', models.CharField(max_length=120)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.BooleanField(help_text='Выделение цветом в общем списке')),
                ('blank', models.BooleanField(help_text='Просмотр в активном окне')),
                ('oil', models.PositiveSmallIntegerField(help_text='Время просмотра сайта')),
                ('price', models.PositiveSmallIntegerField(help_text='Цена за 1000 просмотров (руб.)')),
            ],
        ),
        migrations.AddField(
            model_name='surfingsite',
            name='tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surfing.Tariff'),
        ),
    ]
