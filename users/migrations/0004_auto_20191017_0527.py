# Generated by Django 2.2.5 on 2019-10-17 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190925_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='new_default.jpg', upload_to='profile_pics'),
        ),
    ]