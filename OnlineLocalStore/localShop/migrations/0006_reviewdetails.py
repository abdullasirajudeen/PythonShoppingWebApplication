# Generated by Django 3.0.4 on 2020-06-18 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
        ('localShop', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviewDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(default=1)),
                ('review', models.CharField(default='', max_length=200)),
                ('productid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
                ('userid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]