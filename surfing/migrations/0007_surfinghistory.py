# Generated by Django 2.0.3 on 2018-04-20 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surfing', '0006_surfingsite_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurfingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surfing.SurfingSite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
