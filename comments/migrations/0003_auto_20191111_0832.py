# Generated by Django 2.2.5 on 2019-11-11 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20191108_0857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
    ]