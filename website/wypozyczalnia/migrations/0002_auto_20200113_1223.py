# Generated by Django 3.0 on 2020-01-13 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wypozyczalnia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.IntegerField(),
        ),
    ]
