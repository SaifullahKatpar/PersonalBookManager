# Generated by Django 2.1.7 on 2019-03-04 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20190224_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(help_text='author(s)', related_name='author', to='catalog.Author'),
        ),
    ]
