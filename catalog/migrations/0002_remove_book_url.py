# Generated by Django 2.1.7 on 2019-02-16 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='url',
        ),
    ]