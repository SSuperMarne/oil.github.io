# Generated by Django 2.0.3 on 2018-03-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_clientfactory_clienttower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название баннера. Оно будет видно только вам.', max_length=64, unique=True)),
                ('url', models.URLField(help_text='Укажите URL-адрес, куда будет перенаправлять баннер после клика.')),
                ('img', models.ImageField(help_text='Загрузите изображение баннера', upload_to='banners')),
            ],
        ),
        migrations.AlterField(
            model_name='factory',
            name='img',
            field=models.ImageField(help_text='Изображение завода', upload_to='factories'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='name',
            field=models.CharField(help_text='Укажите название завода', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='factory',
            name='price',
            field=models.IntegerField(help_text='Цена за 1 шт. (укажите число)'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='tower_id',
            field=models.IntegerField(help_text='Идентификатор связанной вышки в БД'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='donated',
            field=models.IntegerField(help_text='Всего внесено в проект (руб.)'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='exchanged',
            field=models.IntegerField(help_text='Всего выведено средств (руб.)'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='oil',
            field=models.IntegerField(help_text='Всего единиц нефти добыто'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='tower',
            field=models.IntegerField(help_text='Всего построенных вышек'),
        ),
        migrations.AlterField(
            model_name='tower',
            name='img',
            field=models.ImageField(help_text='Изображение вышки', upload_to='towers'),
        ),
        migrations.AlterField(
            model_name='tower',
            name='name',
            field=models.CharField(help_text='Укажите название вышки', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='tower',
            name='oil',
            field=models.IntegerField(help_text='Производительность нефти в час (укажите число)'),
        ),
        migrations.AlterField(
            model_name='tower',
            name='price',
            field=models.IntegerField(help_text='Цена за 1 шт. (укажите число)'),
        ),
    ]