# Generated by Django 3.1.4 on 2022-05-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeproduct',
            name='url',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
