# Generated by Django 3.0.4 on 2020-05-03 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('ptype', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('stock', models.IntegerField()),
                ('price', models.IntegerField()),
                ('img1', models.ImageField(upload_to='localshop/pics')),
                ('img2', models.ImageField(default='default.jpg', upload_to='localshop/pics')),
                ('img3', models.ImageField(default='default.jpg', upload_to='localshop/pics')),
                ('offer', models.BooleanField(default=False)),
                ('isactive', models.BooleanField(default=True)),
                ('offerprice', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]